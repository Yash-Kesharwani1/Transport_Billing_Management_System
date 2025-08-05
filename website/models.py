import uuid
from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField()
    user_email = models.CharField()
    user_mobile = models.CharField()
    user_password = models.CharField()
    user_image = models.ImageField(upload_to='static/user/user_profile_image/', blank=True)


class Owner(models.Model):
    owner_name = models.CharField()
    owner_mobile = models.CharField()
    owner_address = models.TextField()
    owner_type = models.CharField()
    balance_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.owner_name

class DeletedOwner(models.Model):
    owner_name = models.CharField()
    owner_mobile = models.CharField()
    owner_address = models.TextField()
    owner_type = models.CharField()
    balance_amount = models.IntegerField(default=0)

# 
class BookVehicle(models.Model):
    vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE)
    from_city = models.CharField(blank=True)
    to_city = models.CharField(blank=True)
    total_hire = models.IntegerField(default=0)
    advance_amount = models.IntegerField(default=0)
    balance_amount = models.IntegerField(default=0)
    to_pay_amount = models.IntegerField(default=0)

class DeletedBookVehicle(models.Model):
    vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE)
    from_city = models.CharField(blank=True)
    to_city = models.CharField(blank=True)
    total_hire = models.IntegerField(default=0)
    advance_amount = models.IntegerField(default=0)
    balance_amount = models.IntegerField(default=0)
    to_pay_amount = models.IntegerField(default=0)

class VehicleType(models.Model):
    vehicle_type = models.CharField()

    def __str__(self):
        return self.vehicle_type
    
class DeletedVehicleType(models.Model):
    vehicle_type = models.CharField()

    def __str__(self):
        return self.vehicle_type

class Vehicle(models.Model):
    vehicle_number = models.CharField()
    owner = models.ForeignKey("Owner", on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey("VehicleType", on_delete=models.CASCADE)
    # total_hire = models.IntegerField()
    # advance_amount = models.IntegerField()
    balance_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.vehicle_number} - {self.owner.owner_name}"

class DeletedVehicle(models.Model):
    vehicle_number = models.CharField()
    owner = models.ForeignKey("Owner", on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey("VehicleType", on_delete=models.CASCADE)
    # total_hire = models.IntegerField()
    # advance_amount = models.IntegerField()
    balance_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.vehicle_number} - {self.owner.owner_name}"



class Party(models.Model):
    party_name = models.CharField()
    party_mobile = models.CharField()
    party_email = models.CharField()
    party_address = models.TextField()
    party_city = models.CharField()
    party_gst_number = models.CharField()
    party_pending_amt = models.IntegerField(default=0)

    def __str__(self):
        return self.party_name

class DeletedParty(models.Model):
    party_name = models.CharField()
    party_mobile = models.CharField()
    party_email = models.CharField()
    party_address = models.TextField()
    party_city = models.CharField()
    party_gst_number = models.CharField()
    party_pending_amt = models.IntegerField(default=0)

    def __str__(self):
        return self.party_name


class Booking(models.Model):
    
    booking_number = models.CharField()

    booking_date = models.DateField(auto_now_add=True)
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey('VehicleType', on_delete=models.CASCADE, blank=True)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    loading_date = models.DateField(auto_now_add=True)
    unloading_date = models.DateField(auto_now_add=True)
    from_city = models.CharField()
    to_city = models.CharField()
    total_hire = models.IntegerField()
    advance_amount = models.IntegerField()
    balance_amount = models.IntegerField()
    commission = models.IntegerField()
    cash = models.IntegerField()
    online = models.IntegerField()
    transaction_id = models.CharField()
    utr = models.CharField() 
    local = models.IntegerField()
    hamali = models.IntegerField()
    tds = models.IntegerField()
    st_charges = models.IntegerField()
    other_charges = models.IntegerField()
    remark = models.CharField()
    sub_total = models.IntegerField()
    previous_amount = models.IntegerField()
    pending_amount = models.IntegerField()
    # The amount pay to vehicle owner
    total_hire_to_pay_to_vehicle = models.IntegerField(default=0)
    advance_amount_to_paid_to_vehicle = models.IntegerField(default=0)
    balance_amount_to_pay_to_vehicle = models.IntegerField(default=0)
    


class DeletedBooking(models.Model):
    
    booking_number = models.CharField()

    booking_date = models.DateField(auto_now_add=True)
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    loading_date = models.DateField(auto_now_add=True)
    unloading_date = models.DateField(auto_now_add=True)
    from_city = models.CharField()
    to_city = models.CharField()
    total_hire = models.IntegerField()
    advance_amount = models.IntegerField()
    balance_amount = models.IntegerField()
    commission = models.IntegerField()
    cash = models.IntegerField()
    online = models.IntegerField()
    transaction_id = models.CharField()
    utr = models.CharField() 
    local = models.IntegerField()
    hamali = models.IntegerField()
    tds = models.IntegerField()
    st_charges = models.IntegerField()
    other_charges = models.IntegerField()
    remark = models.CharField()
    sub_total = models.IntegerField()
    previous_amount = models.IntegerField()
    pending_amount = models.IntegerField()
    # The amount pay to vehicle owner
    total_hire_to_pay_to_vehicle = models.IntegerField(default=0)
    advance_amount_to_paid_to_vehicle = models.IntegerField(default=0)
    balance_amount_to_pay_to_vehicle = models.IntegerField(default=0)
    

    def save(self, *args, **kwargs):
        if not self.booking_number:
            last_booking = Booking.objects.all().order_by('id').last()
            if last_booking:
                last_number = int(last_booking.booking_number[1:])  # Strip "B" and convert to int
                new_number = last_number + 1
            else:
                new_number = 1
            self.booking_number = f'B{new_number:03}'  # e.g., B001, B002, B003
        super().save(*args, **kwargs)



class PaymentRecived(models.Model):

    booking_number = models.CharField()
    
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    cash = models.IntegerField(default=0)
    online = models.IntegerField(default=0)
    transaction_id = models.CharField()
    utr = models.CharField()
    total = models.IntegerField()
    previous_amount = models.IntegerField()
    pending_amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)

class DeletedPaymentRecived(models.Model):
    
    booking_number = models.CharField()

    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    cash = models.IntegerField(default=0)
    online = models.IntegerField(default=0)
    transaction_id = models.CharField()
    utr = models.CharField()
    total = models.IntegerField()
    previous_amount = models.IntegerField()
    pending_amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)



class PaymentSent(models.Model):
    booking_number = models.CharField()
    vehicle_type = models.ForeignKey('VehicleType', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    cash = models.IntegerField(default=0)
    online = models.IntegerField(default=0)
    transaction_id = models.CharField()
    utr = models.CharField()
    total = models.IntegerField()
    previous_amount = models.IntegerField()
    balance_amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)


class DeletedPaymentSent(models.Model):
    booking_number = models.CharField()
    vehicle_type = models.ForeignKey('VehicleType', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    cash = models.IntegerField(default=0)
    online = models.IntegerField(default=0)
    transaction_id = models.CharField()
    utr = models.CharField()
    total = models.IntegerField()
    previous_amount = models.IntegerField()
    balance_amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)


# This is for the Address 

# STATE
class State(models.Model):
    state_name = models.CharField()

# CITY
class City(models.Model):
    city_name = models.CharField()
    state = models.ForeignKey("State", on_delete=models.CASCADE)