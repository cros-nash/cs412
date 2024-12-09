from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count
from django.db import transaction
from .models import Discount, Item, Category, Order, OrderItem, UserProfile
from .forms import (
    UserRegistrationForm,
    ItemForm,
    UserProfileForm,
    UserUpdateForm,
    AddToCartForm,
    UpdateQuantityForm,
)

class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        UserProfile.objects.create(user=user, address=form.cleaned_data["address"])
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def get_success_url(self):
        return self.success_url

class UserLogoutView(LogoutView):
    template_name = "registration/logout.html"

class ItemListView(ListView):
    template_name = "items/item_list.html"
    context_object_name = "items"
    paginate_by = 12

    def get_queryset(self):
        return Item.objects.filter(quantity_available__gt=0).order_by("-date_listed")

class ItemDetailView(DetailView):
    template_name = "items/item_detail.html"
    model = Item
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_to_cart_form"] = AddToCartForm()
        return context

class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = "items/item_form.html"
    form_class = ItemForm

    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, "Item listed successfully.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("item_detail", kwargs={"pk": self.object.pk})

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "items/item_form.html"
    model = Item
    form_class = ItemForm

    def get_queryset(self):
        return Item.objects.filter(seller=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Item updated successfully.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("item_detail", kwargs={"pk": self.object.pk})
    

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "items/item_confirm_delete.html"
    success_url = reverse_lazy("item_list")

    def get_queryset(self):
        return Item.objects.filter(seller=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Item deleted successfully.")
        return super().delete(request, *args, **kwargs)

class SearchView(ListView):
    template_name = "search_results.html"
    context_object_name = "items"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Item.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            quantity_available__gt=0,
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=kwargs["pk"])
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            if quantity > item.quantity_available:
                messages.error(
                    request,
                    f"Requested quantity exceeds available stock ({item.quantity_available}).",
                )
                return redirect("item_detail", item.pk)

            with transaction.atomic():
                order, _ = Order.objects.get_or_create(buyer=request.user, status="cart")
                order_item, _ = OrderItem.objects.get_or_create(order=order, item=item, defaults={"quantity": 0})
                order_item.quantity += quantity
                order_item.save()

                order.total_amount += item.price * quantity
                order.save()

            messages.success(request, f"Added {quantity} x {item.title} to your cart.")
            return redirect("view_cart")
        else:
            messages.error(request, "Invalid quantity. Please enter a valid number.")
            return redirect("item_detail", item.pk)

class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order, _ = Order.objects.get_or_create(buyer=self.request.user, status="cart")
        order_items = OrderItem.objects.filter(order=order)
        total = order.total_amount
        update_quantity_forms = {
            order_item.id: UpdateQuantityForm(initial={"quantity": order_item.quantity})
            for order_item in order_items
        }
        context.update(
            {
                "order": order,
                "order_items": order_items,
                "total": total,
                "update_quantity_forms": update_quantity_forms,
            }
        )
        return context

class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(buyer=request.user, status="cart")
        order_items = OrderItem.objects.filter(order=order)
        updated = False

        remove_discount = request.POST.get("remove_discount")
        if remove_discount:
            if order.discount:
                order.discount = None
                order.discount_amount = 0.0
                order.calculate_total()
                messages.success(request, "Discount removed successfully.")
            else:
                messages.info(request, "No discount to remove.")
            return redirect("view_cart")

        remove_item_id = request.POST.get("remove_item")
        if remove_item_id:
            try:
                with transaction.atomic():
                    order_item = get_object_or_404(OrderItem, id=remove_item_id, order=order)
                    order_item.delete()
                    order.calculate_total()
                    messages.success(request, "Item removed from your cart.")
            except Exception as e:
                messages.error(request, "An error occurred while removing the item from your cart.")
            return redirect("view_cart")

        for order_item in order_items:
            quantity_key = f"quantity_{order_item.id}"
            if quantity_key in request.POST:
                try:
                    new_quantity = int(request.POST[quantity_key])
                    if new_quantity != order_item.quantity:
                        if new_quantity > order_item.item.quantity_available:
                            messages.error(
                                request,
                                f"Requested quantity for {order_item.item.title} exceeds available stock ({order_item.item.quantity_available}).",
                            )
                            continue
                        order_item.quantity = new_quantity
                        order_item.save()
                        updated = True
                except ValueError:
                    messages.error(request, f"Invalid quantity entered for {order_item.item.title}.")
                    continue

        discount_code = request.POST.get("discount_code")
        if discount_code and not order.discount:
            try:
                discount = Discount.objects.get(code__iexact=discount_code, active=True)
                if not discount.is_valid():
                    messages.error(request, "This discount code is invalid or has expired.")
                else:
                    order.discount = discount
                    if discount.discount_type == "percentage":
                        order.discount_amount = (discount.amount / 100) * order.calculate_original_total
                    elif discount.discount_type == "fixed":
                        order.discount_amount = discount.amount
                    order.calculate_total()
                    discount.used_count += 1
                    discount.save()
                    messages.success(request, f'Discount "{discount.code}" applied successfully.')
            except Discount.DoesNotExist:
                messages.error(request, "Invalid discount code.")
            except Exception as e:
                messages.error(request, "An error occurred while applying the discount code.")

        if updated:
            order.calculate_total()
            messages.success(request, "Cart updated successfully.")
        else:
            if not discount_code and not remove_item_id and not remove_discount:
                messages.info(request, "No changes made to the cart.")

        return redirect("view_cart")

class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "checkout.html"

    def get_order(self):
        return get_object_or_404(Order, buyer=self.request.user, status="cart")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.get_order()
        return context
    
    def post(self, request, *args, **kwargs):
        order = self.get_order()
        with transaction.atomic():
            order.status = "shipped"
            order.save()

            for order_item in OrderItem.objects.filter(order=order):
                item = order_item.item
                if item.quantity_available >= order_item.quantity:
                    item.quantity_available -= order_item.quantity
                    item.save()
                else:
                    messages.error(request, f"Not enough stock for {item.title}.")
                    return redirect("view_cart")

        messages.success(request, "Checkout successful! Your order has been placed.")
        return redirect("order_history")

class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = "order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).exclude(status="cart").order_by("-order_date")

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        items_for_sale = Item.objects.filter(seller=user)
        purchase_orders = Order.objects.filter(buyer=user).exclude(status="cart").order_by("-order_date")

        orders_with_totals = []
        for order in purchase_orders:
            order_items = OrderItem.objects.filter(order=order)
            total_amount = sum(order_item.item.price * order_item.quantity for order_item in order_items)
            order.total_amount_calculated = total_amount
            orders_with_totals.append(order)

        context.update(
            {
                "user": user,
                "user_profile": user_profile,
                "items_for_sale": items_for_sale,
                "purchase_orders": orders_with_totals,
            }
        )
        return context
class UpdateProfileView(LoginRequiredMixin, View):
    template_name = "update_profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)
        return render(request, self.template_name, {"user_form": user_form, "profile_form": profile_form})

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
        return render(request, self.template_name, {"user_form": user_form, "profile_form": profile_form})

class ChangePasswordView(PasswordChangeView):
    template_name = "change_password.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        messages.success(self.request, "Your password was successfully updated!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class CategoryListView(ListView):
    template_name = "categories/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.annotate(
            in_stock_item_count=Count("item", filter=Q(item__quantity_available__gt=0))
        ).filter(in_stock_item_count__gt=0).order_by("name")
        
class CategoryDetailView(DetailView):
    template_name = "categories/category_detail.html"
    model = Category
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_option = self.request.GET.get("sort", "")
        items = Item.objects.filter(category=self.object, quantity_available__gt=0)

        if sort_option == "price_asc":
            items = items.order_by("price")
        elif sort_option == "price_desc":
            items = items.order_by("-price")
        elif sort_option == "date_new":
            items = items.order_by("-date_listed")
        elif sort_option == "date_old":
            items = items.order_by("date_listed")
        else:
            items = items.order_by("-date_listed")

        context["items"] = items
        return context
