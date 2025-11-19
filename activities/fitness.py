"""
 Module Name: fitness.py
 Author: thibault2705 
 Date: 2025-11-18
 Description:
 """
import pandas as pd
from garmindb import GarminConnectConfigManager

from garmindb.garmindb import (
    Activities,
    ActivitiesDb
)


class Fitness:
    config_manager = GarminConnectConfigManager()
    db_params_dict = config_manager.get_db_params()
    garmin_act_db = ActivitiesDb(db_params_dict)

    @classmethod
    def get_all_activities(cls):
        activities = Activities.get_by_sport(cls.garmin_act_db, "fitness_equipment")

        # Parse garmindb.garmindb.activities_db.Activities to activities.fitness.FitnessActivity
        return [FitnessActivity(act) for act in activities]

    @classmethod
    def get_all_activities_df(cls):
        fitness_activities = cls.get_all_activities()

        return pd.DataFrame([vars(act) for act in fitness_activities])


class FitnessActivity(Activities):

    def __init__(self, activity: Activities):
        self.id = activity.activity_id
        self.name = activity.name
        self.sport = activity.sport
        self.sub_sport = activity.sub_sport
        self.training_load = activity.training_load
        self.training_effect = activity.training_effect
        self.anaerobic_training_effect = activity.anaerobic_training_effect
        self.start_time = activity.start_time
        self.stop_time = activity.stop_time
        self.moving_time = activity.moving_time
        self.avg_hr = activity.avg_hr
        self.max_hr = activity.max_hr
        self.calories = activity.calories
        self.hrz_1 = activity.hrz_1_hr
        self.hrz_2 = activity.hrz_2_hr
        self.hrz_3 = activity.hrz_3_hr
        self.hrz_4 = activity.hrz_4_hr
        self.hrz_5 = activity.hrz_5_hr
        self.hrz_1_time = activity.hrz_1_time
        self.hrz_2_time = activity.hrz_2_time
        self.hrz_3_time = activity.hrz_3_time
        self.hrz_4_time = activity.hrz_4_time
        self.hrz_5_time = activity.hrz_5_time

    def to_json(self):
        return {
            "id": self.activity_id,
            "name": self.name,
            "sport": self.sport,
            "sub_sport": self.sub_sport,
            "training_load": self.training_load,
            "training_effect": self.training_effect,
            "anaerobic_training_effect": self.anaerobic_training_effect,
            "moving_time": self.moving_time,
            "avg_hr": self.avg_hr,
            "max_hr": self.max_hr,
            "calories": self.calories,
            "hrz_1": self.hrz_1_hr,
            "hrz_2": self.hrz_2_hr,
            "hrz_3": self.hrz_3_hr,
            "hrz_4": self.hrz_4_hr,
            "hrz_5": self.hrz_5_hr,
            "hrz_1_time": self.hrz_1_time,
            "hrz_2_time": self.hrz_2_time,
            "hrz_3_time": self.hrz_3_time,
            "hrz_4_time": self.hrz_4_time,
            "hrz_5_time": self.hrz_5_time
        }

    def get_id(self):
        return self.activity_id

    def get_name(self):
        return self.name

    def get_sport(self):
        return self.sport

    def get_sub_sport(self):
        return self.sub_sport

    def get_training_load(self):
        return self.training_load

    def get_training_effect(self):
        return self.training_effect

    def get_anaerobic_training_effect(self):
        return self.anaerobic_training_effect

    def get_moving_time(self):
        return self.moving_time

    def get_avg_hr(self):
        return self.avg_hr

    def get_max_hr(self):
        return self.max_hr

    def get_calories(self):
        return self.calories

    def get_hrz_1(self):
        return self.hrz_1_hr

    def get_hrz_2(self):
        return self.hrz_2_hr

    def get_hrz_3(self):
        return self.hrz_3_hr

    def get_hrz_4(self):
        return self.hrz_4_hr

    def get_hrz_5(self):
        return self.hrz_5_hr

    def get_hrz_1_time(self):
        return self.hrz_1_time

    def get_hrz_2_time(self):
        return self.hrz_2_time

    def get_hrz_3_time(self):
        return self.hrz_3_time

    def get_hrz_4_time(self):
        return self.hrz_4_time

    def get_hrz_5_time(self):
        return self.hrz_5_time
