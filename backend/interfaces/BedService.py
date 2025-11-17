from db_model import db, Bed

class BedService:

    # CREATE
    @staticmethod
    def create_bed(data):
        """Create a new bed. Allow manual bed_No but check for collisions."""
        try:
            custom_id = data.get("bed_No")

            # Safety check: prevent ID collision
            if custom_id is not None:
                existing = Bed.query.get(custom_id)
                if existing:
                    raise ValueError(f"Bed number {custom_id} already exists.")

            new_bed = Bed(
                bed_No=custom_id,
                ward_No=data.get("ward_No")
            )

            db.session.add(new_bed)
            db.session.commit()
            return new_bed.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_bed(bed_no, data):
        """Update an existing bed."""
        bed = Bed.query.get(bed_no)
        if not bed:
            return None

        try:
            for key, value in data.items():
                if key != "bed_No" and hasattr(bed, key):  
                    # bed_No should not be changed
                    setattr(bed, key, value)

            db.session.commit()
            return bed.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_bed(bed_no):
        """Delete bed by ID."""
        bed = Bed.query.get(bed_no)
        if not bed:
            return False

        try:
            db.session.delete(bed)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY ID
    @staticmethod
    def get_bed_by_id(bed_no):
        bed = Bed.query.get(bed_no)
        return bed.to_dict() if bed else None

    # GET BY WARD
    @staticmethod
    def get_beds_by_ward(ward_no):
        beds = Bed.query.filter_by(ward_No=ward_no).all()
        return [b.to_dict() for b in beds]

    # GET ALL
    @staticmethod
    def get_all_beds():
        beds = Bed.query.all()
        return [b.to_dict() for b in beds]
