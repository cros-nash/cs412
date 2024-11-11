from django.db import IntegrityError, models

class Voter(models.Model):
    '''
    Store/represent the data from a voter in newton_voters.csv.
    '''
    last_name = models.TextField()
    first_name = models.TextField()
    
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip = models.TextField()

    dob = models.DateField()
    registration_date = models.DateField()

    party = models.TextField()
    precinct = models.IntegerField()
    
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.street_name}, {self.apartment_number}, {self.zip}), {self.dob}, {self.party}, {self.voter_score}'
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()
    
    filename = 'voter_analytics/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Result object with this record from CSV
            voters = Voter(last_name=fields[1],
                            first_name=fields[2],
                            
                            street_number = fields[3],
                            street_name = fields[4],
                            apartment_number = fields[5],
                            zip = fields[6],
                            
                            dob = fields[7],
                            registration_date = fields[8],
                            
                            party = fields[9],
                            precinct = fields[10],
                        
                            v20state = fields[11],
                            v21town = fields[12],
                            v21primary = fields[13],
                            v22general = fields[14],
                            v23town = fields[15],
                            
                            voter_score = fields[16],
                        )
        
            voters.save() # commit to database
            print(f'Created result: {voters}')
            
        except (ValueError, IntegrityError) as e:
                print(f"Skipped: {fields} due to error: {e}")
    
    print(f'Done. Created {len(Voter.objects.all())} Results.')