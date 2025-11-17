from db_model import db, Room

class RoomService:

    # CREATE
    @staticmethod
    def create_room(data):
        """Create a new room (manual room_No allowed with collision safety)."""
        try:
            custom_id = data.get("room_No")

            # Collision check
            if custom_id is not None:
                existing = Room.query.get(custom_id)
                if existing:
                    raise ValueError(f"Room number {custom_id} already exists.")

            new_room = Room(
                room_No=custom_id,
                dept_Id=data.get("dept_Id"),
                room_Type=data.get("room_Type")
            )

            db.session.add(new_room)
            db.session.commit()
            return new_room.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # UPDATE
    @staticmethod
    def update_room(room_no, data):
        room = Room.query.get(room_no)
        if not room:
            return None

        try:
            for key, value in data.items():
                if key != "room_No" and hasattr(room, key):
                    setattr(room, key, value)

            db.session.commit()
            return room.to_dict()

        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def delete_room(room_no):
        room = Room.query.get(room_no)
        if not room:
            return False

        try:
            db.session.delete(room)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise e

    # GET BY DEPARTMENT (sorted alphabetically by room_Type)
    @staticmethod
    def get_rooms_by_department(dept_id):
        rooms = (
            Room.query
            .filter_by(dept_Id=dept_id)
            .order_by(Room.room_Type.asc())
            .all()
        )
        return [r.to_dict() for r in rooms]

    # GET BY ROOM TYPE (sorted alphabetically)
    @staticmethod
    def get_rooms_by_type(room_type):
        rooms = (
            Room.query
            .filter_by(room_Type=room_type)
            .order_by(Room.room_No.asc())
            .all()
        )
        return [r.to_dict() for r in rooms]
    

    # GET BY ID
    @staticmethod
    def get_room_by_id(room_no):
        room = Room.query.get(room_no)
        return room.to_dict() if room else None
    
    # GET ALL (sorted by room_No)
    @staticmethod
    def get_all_rooms():
        rooms = Room.query.order_by(Room.room_No.asc()).all()
        return [r.to_dict() for r in rooms]