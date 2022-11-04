from sqlalchemy.orm import Session
from app.models.base_season_pond import BaseSeasonPonds
from app.core.database import get_db
from datetime import datetime, timedelta
from app.models.dead_fish_diary import DeadFishDiaries


def job():
    new_day = datetime.now()
    if new_day.hour == 0 and new_day.minute == 0:
        print(f"Bắt đầu chương trình tạo cá chết lúc {new_day.hour}:{new_day.minute} {new_day.day}/{new_day.month}/{new_day.year}")
        db: Session = next(get_db())
        today = datetime.now().date()
        print(f"today: {today}")
        the_day_before = today - timedelta(days=1)

        dead_fish_diaries = db.query(DeadFishDiaries)\
                            .distinct(DeadFishDiaries.pond_id)\
                            .join(BaseSeasonPonds, DeadFishDiaries.pond_id == BaseSeasonPonds.pond_id)\
                            .filter(BaseSeasonPonds.status.in_(['Đang nuôi','Đang thu hoạch','Đã thu hoạch','Đang vệ sinh','Đã vệ sinh','Đang kiểm tra','Đã kiểm tra']))\
                            .filter(DeadFishDiaries.in_date == the_day_before).all()

        for dead_fish_diary in dead_fish_diaries:
            existing = db.query(DeadFishDiaries).filter(DeadFishDiaries.pond_id == dead_fish_diary.pond_id, DeadFishDiaries.in_date == today).first()

            if not existing:
                new_dead_fish_diary = DeadFishDiaries(
                    pond_id=dead_fish_diary.pond_id,
                    quantity=0,
                    mass=0,
                    in_date=today,
                    average_weight=dead_fish_diary.average_weight,
                    accumulated_loss=dead_fish_diary.accumulated_loss,
                    accumulated_exist=dead_fish_diary.accumulated_exist,
                    estimated_volume=dead_fish_diary.estimated_volume
                )
                db.add(new_dead_fish_diary)
                db.flush()
                print(new_dead_fish_diary.id)    
        db.commit()
        print("Kết thúc chương trình thành công.")



