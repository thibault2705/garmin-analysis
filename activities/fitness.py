"""
 Module Name: fitness.py
 Author: thibault2705 
 Date: 2025-11-18
 Description:
 """
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from datetime import datetime
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

        df = pd.DataFrame([vars(act) for act in fitness_activities])

        sub_sport_map = {
            'strength_training': 'Strength Training',
            'cardio_training': 'Cardio Training',
            'hiit': 'HIIT'
        }
        df['sub_sport_label'] = df['sub_sport'].map(sub_sport_map)

        return df

    @classmethod
    def _get_timestamp(cls):
        timestamp = datetime.now()
        return timestamp.strftime("%Y%m%d%H%M%S")

    @classmethod
    def _convert_to_minutes(cls, time_value):
        if pd.isna(time_value):
            return np.nan

        time_str = str(time_value)

        time_delta = pd.to_timedelta(time_str)
        return time_delta.total_seconds() / 60.0

    @classmethod
    def plot_monthly_calories_line_chart(cls):
        df = cls.get_all_activities_df()
        df_monthly = df.set_index('start_time')['calories'].resample('ME').sum().fillna(0)

        plt.figure(figsize=(8, 4))
        plt.plot(df_monthly.index, df_monthly.values, marker='o', linestyle='-', color='chocolate')
        plt.xticks(rotation=90)
        plt.title('Monthly Total Calories Burned Over Time')
        plt.xlabel('Month End Date')
        plt.ylabel('Total Calories')
        plt.xticks(rotation=45)
        plt.tight_layout()

        file_name = f"{cls._get_timestamp()}_monthly_calories_line_chart.png"
        plt.savefig(f'../charts/{file_name}')
        plt.show()

        print(f"Generated {file_name}")

    @classmethod
    def plot_training_load_by_sport_bar_chart(cls):
        df = cls.get_all_activities_df()

        df_sub_sport_load = df.groupby('sub_sport_label')['training_load'].sum().sort_values(ascending=False)

        plt.figure(figsize=(8, 4))
        df_sub_sport_load.plot(kind='bar', color='cornflowerblue')
        plt.xticks(rotation=90)
        plt.xticks(rotation=90)
        plt.title('Total Training Load by Fitness Activity Type')
        plt.xlabel('Fitness Activity Type')
        plt.ylabel('Total Training Load')
        plt.xticks(rotation=0, ha='center')
        plt.tight_layout()

        file_name = f"{cls._get_timestamp()}_training_load_by_sport_bar_chart.png"
        plt.savefig(f'../charts/{file_name}')
        plt.show()

        print(f"Generated {file_name}")


    @classmethod
    def plot_avg_hr_histogram(cls):
        df = cls.get_all_activities_df()
        plt.figure(figsize=(8, 4))

        df['avg_hr'].hist(
            bins=20,
            edgecolor='black',
            color='mediumturquoise',
        )

        plt.title('Distribution of Average Heart Rate (BPM)')
        plt.xlabel('Average Heart Rate (BPM)')
        plt.ylabel('Frequency (Number of Activities)')
        plt.tight_layout()

        file_name = f"{cls._get_timestamp()}_avg_hr_histogram.png"
        plt.savefig(f'../charts/{file_name}')
        plt.show()

        print(f"Generated {file_name}")

    @classmethod
    def plot_hr_load_scatter_chart(cls):
        df = cls.get_all_activities_df()
        rng = np.random.RandomState(0)

        x = df['avg_hr']
        y = df['training_load']
        sizes = df['calories']

        colors = rng.rand(len(x))

        plt.scatter(x,
                    y,
                    c=colors,
                    s=sizes,
                    alpha=0.5,  # transparency
                    cmap='coolwarm')

        plt.title('Relationship: HR vs. Load, Colored and Sized by Calorie Range')
        plt.xlabel('Average Heart Rate (BPM)')
        plt.ylabel('Training Load')
        plt.colorbar();  # show color scale

        file_name = f"{cls._get_timestamp()}_relationship_buble_chart.png"
        plt.savefig(f'../charts/{file_name}')
        plt.show()

        print(f"Generated {file_name}")

    @classmethod
    def plot_activities_proportions_pie_chart(cls):
        df = cls.get_all_activities_df()
        sub_sport_counts = df['sub_sport'].value_counts()

        plt.figure(figsize=(5, 5))

        plt.pie(
            sub_sport_counts.values,  # The counts (values)
            labels=sub_sport_counts.index,  # The sport names (labels)
            autopct='%1.1f%%',  # Format to display percentages (e.g., 10.5%)
            startangle=90,  # Start the first slice at the top
            colors=sns.color_palette("Set2"),  # Use a pastel color palette
            wedgeprops={'edgecolor': 'black'}  # Add borders to slices for clarity
        )

        plt.title('Proportion of Activities by Fitness Activity Type', fontsize=16)
        plt.tight_layout()

        file_name = f"{cls._get_timestamp()}_activities_proportions_pie_chart.png"
        plt.savefig(f'../charts/{file_name}')
        plt.show()

        print(f"Generated {file_name}")

    @classmethod
    def plot_stress_duration_scatter_chart(cls):
        df = cls.get_all_activities_df()
        df['duration_minutes'] = df['moving_time'].apply(cls._convert_to_minutes)

        plt.figure(figsize=(10, 6))

        sns.scatterplot(
            data=df,
            x='duration_minutes',
            y='training_load',
            hue='sub_sport_label',
            s=200,
            alpha=0.7
        )

        plt.title('Training Load Profile by Activity Type')
        plt.xlabel('Activity Duration (Minutes)')
        plt.ylabel('Training Load Score (Stress)')
        plt.legend(title='Fitness Type', loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.6)

        file_name = f"{cls._get_timestamp()}_stress_duration_scatter_chart.png"
        plt.savefig(f'../charts/{file_name}')
        plt.show()

        print(f"Generated {file_name}")


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
