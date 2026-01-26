"""
Seed database with realistic test data
Run this after migrations: python scripts/seed_data.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Member, Drug, Pharmacy, Claim, Formulary
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal

fake = Faker()


def create_members(count=100):
    """Create fake members"""
    print(f"Creating {count} members...")
    members = []
    
    plan_types = ['PPO', 'HMO', 'High Deductible', 'EPO']
    
    for i in range(count):
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=85)
        effective_date = fake.date_between(start_date='-2y', end_date='today')
        
        member = Member(
            member_id=f"MBR{str(i+1).zfill(6)}",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=birth_date,
            gender=random.choice(['Male', 'Female', 'Other']),
            email=fake.email(),
            phone=fake.phone_number()[:20],
            address_line1=fake.street_address(),
            city=fake.city(),
            state=fake.state_abbr(),
            zip_code=fake.zipcode(),
            plan_type=random.choice(plan_types),
            group_id=f"GRP{random.randint(1000, 9999)}",
            effective_date=effective_date,
            is_active=random.choice([True, True, True, False])  # 75% active
        )
        members.append(member)
        
        if (i + 1) % 20 == 0:
            print(f"  Created {i + 1} members")
    
    db.session.bulk_save_objects(members)
    db.session.commit()
    print(f"✓ Created {count} members")
    return Member.query.all()


def create_drugs(count=200):
    """Create fake drugs"""
    print(f"Creating {count} drugs...")
    drugs = []
    
    therapeutic_classes = [
        'Antidiabetic', 'Antihypertensive', 'Antibiotic', 'Antidepressant',
        'Analgesic', 'Anticoagulant', 'Lipid-Lowering', 'Antiasthmatic',
        'Anticonvulsant', 'Antipsychotic'
    ]
    
    dosage_forms = ['Tablet', 'Capsule', 'Injection', 'Solution', 'Suspension']
    routes = ['Oral', 'Injection', 'Topical', 'Inhalation']
    
    # Common drug names
    generic_prefixes = ['Ator', 'Simva', 'Met', 'Lisin', 'Amlod', 'Omep', 'Sertra', 'Escit']
    generic_suffixes = ['statin', 'formin', 'opril', 'ipine', 'razole', 'line', 'pram']
    
    for i in range(count):
        is_generic = random.choice([True, True, False])  # 67% generic
        
        if is_generic:
            name = random.choice(generic_prefixes) + random.choice(generic_suffixes)
            generic_name = name
            brand_name = None
        else:
            brand_name = fake.company().split()[0] + random.choice(['x', 'a', 'in', 'ol'])
            generic_name = random.choice(generic_prefixes) + random.choice(generic_suffixes)
            name = brand_name
        
        strength = f"{random.choice([5, 10, 20, 25, 40, 50, 100, 250, 500])}{random.choice(['mg', 'mcg'])}"
        
        # Generic drugs are cheaper
        if is_generic:
            awp = Decimal(random.uniform(10, 150))
        else:
            awp = Decimal(random.uniform(100, 800))
        
        drug = Drug(
            ndc=f"{random.randint(10000, 99999)}-{random.randint(100, 999)}-{random.randint(10, 99)}",
            name=name,
            generic_name=generic_name,
            brand_name=brand_name,
            is_generic=is_generic,
            therapeutic_class=random.choice(therapeutic_classes),
            drug_class=fake.word().capitalize(),
            strength=strength,
            dosage_form=random.choice(dosage_forms),
            route=random.choice(routes),
            manufacturer=fake.company(),
            awp=awp,
            package_size=random.choice([30, 60, 90, 100]),
            is_active=True
        )
        drugs.append(drug)
        
        if (i + 1) % 50 == 0:
            print(f"  Created {i + 1} drugs")
    
    db.session.bulk_save_objects(drugs)
    db.session.commit()
    print(f"✓ Created {count} drugs")
    return Drug.query.all()


def create_pharmacies(count=50):
    """Create fake pharmacies"""
    print(f"Creating {count} pharmacies...")
    pharmacies = []
    
    chains = ['CVS', 'Walgreens', 'Walmart', 'Rite Aid', 'Kroger', None, None]  # Some independent
    pharmacy_types = ['Retail', 'Mail Order', 'Specialty']
    network_tiers = ['Preferred', 'Standard', 'Out-of-Network']
    
    for i in range(count):
        chain = random.choice(chains)
        name = f"{chain} Pharmacy #{random.randint(1000, 9999)}" if chain else f"{fake.city()} Pharmacy"
        
        pharmacy = Pharmacy(
            ncpdp_id=str(random.randint(1000000, 9999999)),
            npi=str(random.randint(1000000000, 9999999999)),
            name=name,
            chain_name=chain,
            phone=fake.phone_number()[:20],
            email=fake.company_email(),
            address_line1=fake.street_address(),
            city=fake.city(),
            state=fake.state_abbr(),
            zip_code=fake.zipcode(),
            latitude=Decimal(str(fake.latitude())),
            longitude=Decimal(str(fake.longitude())),
            pharmacy_type=random.choice(pharmacy_types),
            is_24_hours=random.choice([True, False]),
            accepts_new_patients=True,
            in_network=random.choice([True, True, True, False]),  # 75% in network
            network_tier=random.choice(network_tiers),
            is_active=True
        )
        pharmacies.append(pharmacy)
    
    db.session.bulk_save_objects(pharmacies)
    db.session.commit()
    print(f"✓ Created {count} pharmacies")
    return Pharmacy.query.all()


def create_formulary(drugs):
    """Create formulary entries for drugs"""
    print(f"Creating formulary entries for {len(drugs)} drugs...")
    formulary_entries = []
    
    tier_configs = {
        1: {'name': 'Generic', 'copay_retail': Decimal('10'), 'copay_mail_order': Decimal('20')},
        2: {'name': 'Preferred Brand', 'copay_retail': Decimal('35'), 'copay_mail_order': Decimal('70')},
        3: {'name': 'Non-Preferred Brand', 'copay_retail': Decimal('60'), 'copay_mail_order': Decimal('120')},
        4: {'name': 'Specialty', 'copay_retail': Decimal('100'), 'copay_mail_order': Decimal('200')},
    }
    
    for drug in drugs:
        # Generic drugs get tier 1, brands get 2-4
        if drug.is_generic:
            tier = 1
        else:
            tier = random.choices([2, 3, 4], weights=[0.5, 0.3, 0.2])[0]
        
        config = tier_configs[tier]
        
        formulary = Formulary(
            drug_id=drug.id,
            tier=tier,
            tier_name=config['name'],
            is_covered=True,
            requires_prior_auth=tier >= 3 and random.random() < 0.3,
            requires_step_therapy=tier >= 3 and random.random() < 0.2,
            quantity_limit=random.choice([None, 30, 60, 90]),
            copay_retail=config['copay_retail'],
            copay_mail_order=config['copay_mail_order'],
            coinsurance_rate=Decimal('0.20') if tier == 4 else None,
            effective_date=datetime(2024, 1, 1).date(),
            coverage_notes=None
        )
        formulary_entries.append(formulary)
    
    db.session.bulk_save_objects(formulary_entries)
    db.session.commit()
    print(f"✓ Created formulary entries")


def create_claims(members, drugs, pharmacies, count=1000):
    """Create fake claims"""
    print(f"Creating {count} claims...")
    claims = []
    
    statuses = ['paid', 'paid', 'paid', 'approved', 'pending', 'denied']  # Most paid
    
    start_date = datetime.now().date() - timedelta(days=180)
    
    for i in range(count):
        member = random.choice(members)
        drug = random.choice(drugs)
        pharmacy = random.choice(pharmacies)
        
        fill_date = start_date + timedelta(days=random.randint(0, 180))
        quantity = Decimal(random.choice([30, 60, 90]))
        days_supply = int(quantity)  # Simplified
        
        # Calculate costs
        if drug.awp:
            base_cost = drug.awp * (quantity / 30)  # Normalize to 30-day supply
        else:
            base_cost = Decimal(random.uniform(50, 500))
        
        dispensing_fee = Decimal('2.50')
        sales_tax = base_cost * Decimal('0.07')
        submitted_amount = base_cost + dispensing_fee + sales_tax
        
        # Apply copay based on generic status
        if drug.is_generic:
            member_copay = Decimal(random.choice([5, 10, 15]))
        else:
            member_copay = Decimal(random.choice([25, 35, 50]))
        
        plan_paid = submitted_amount - member_copay
        
        status = random.choice(statuses)
        
        claim = Claim(
            claim_number=f"CLM{str(i+1).zfill(8)}",
            rx_number=f"RX{random.randint(100000, 999999)}",
            member_id=member.id,
            drug_id=drug.id,
            pharmacy_id=pharmacy.id,
            fill_date=fill_date,
            service_date=fill_date,
            quantity=quantity,
            days_supply=days_supply,
            refills_authorized=random.choice([0, 1, 2, 3, 5]),
            refill_number=0,
            prescriber_npi=str(random.randint(1000000000, 9999999999)),
            prescriber_name=f"Dr. {fake.last_name()}",
            submitted_amount=submitted_amount,
            ingredient_cost=base_cost,
            dispensing_fee=dispensing_fee,
            sales_tax=sales_tax,
            plan_paid_amount=plan_paid if status in ['paid', 'approved'] else None,
            member_copay=member_copay,
            member_coinsurance=None,
            deductible_applied=None,
            total_cost=submitted_amount,
            status=status,
            rejection_code='75' if status == 'denied' else None,
            rejection_reason='Prior authorization required' if status == 'denied' else None,
            is_generic_substitution=not drug.is_generic and random.random() < 0.1,
            requires_prior_auth=random.random() < 0.05,
            is_compound=False,
            is_specialty=random.random() < 0.05,
            submitted_at=datetime.combine(fill_date, datetime.min.time()),
            processed_at=datetime.combine(fill_date, datetime.min.time()) + timedelta(hours=2) if status != 'pending' else None,
            paid_at=datetime.combine(fill_date, datetime.min.time()) + timedelta(days=7) if status == 'paid' else None
        )
        claims.append(claim)
        
        if (i + 1) % 200 == 0:
            print(f"  Created {i + 1} claims")
            db.session.bulk_save_objects(claims)
            db.session.commit()
            claims = []
    
    if claims:
        db.session.bulk_save_objects(claims)
        db.session.commit()
    
    print(f"✓ Created {count} claims")


def seed_database():
    """Main seeding function"""
    print("\n" + "="*50)
    print("SEEDING DATABASE WITH TEST DATA")
    print("="*50 + "\n")
    
    # Create application context
    app = create_app()
    
    with app.app_context():
        # Check if data already exists
        if Member.query.first():
            print("⚠️  Database already contains data!")
            response = input("Do you want to clear and reseed? (yes/no): ")
            if response.lower() != 'yes':
                print("Aborted.")
                return
            
            print("\nClearing existing data...")
            Claim.query.delete()
            Formulary.query.delete()
            Drug.query.delete()
            Pharmacy.query.delete()
            Member.query.delete()
            db.session.commit()
            print("✓ Cleared existing data\n")
        
        # Seed data
        members = create_members(100)
        drugs = create_drugs(200)
        pharmacies = create_pharmacies(50)
        create_formulary(drugs)
        create_claims(members, drugs, pharmacies, 1000)
        
        # Print summary
        print("\n" + "="*50)
        print("DATABASE SEEDING COMPLETE!")
        print("="*50)
        print(f"Members:     {Member.query.count()}")
        print(f"Drugs:       {Drug.query.count()}")
        print(f"Pharmacies:  {Pharmacy.query.count()}")
        print(f"Formulary:   {Formulary.query.count()}")
        print(f"Claims:      {Claim.query.count()}")
        print("="*50 + "\n")


if __name__ == '__main__':
    seed_database()
