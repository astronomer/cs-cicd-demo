from datetime import datetime, timedelta
from typing import Dict

# Airflow operators are templates for tasks and encompass the logic that your DAG will actually execute.
# To use an operator in your DAG, you first have to import it.
# To learn more about operators, see: https://registry.astronomer.io/.

from airflow.decorators import dag, task # DAG and task decorators for interfacing with the TaskFlow API
from airflow.models.baseoperator import chain # A function that sets sequential dependencies between tasks including lists of tasks.
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.weekday import BranchDayOfWeekOperator
from airflow.utils.edgemodifier import Label # Used to label node edges in the Airflow UI
from airflow.utils.task_group import TaskGroup # Used to group tasks together in the Graph view of the Airflow UI
from airflow.utils.trigger_rule import TriggerRule # Used to change how an Operator is triggered
from airflow.utils.weekday import WeekDay # Used to determine what day of the week it is

DAY_ACTIVITY_MAPPING = {
    "monday": {"is_weekday": True, "activity": "guitar lessons"},
    "tuesday": {"is_weekday": True, "activity": "studying"},
    "wednesday": {"is_weekday": True, "activity": "soccer practice"},
    "thursday": {"is_weekday": True, "activity": "contributing to Airflow"},
    "friday": {"is_weekday": True, "activity": "family dinner"},
    "saturday": {"is_weekday": False, "activity": "going to the beach"},
    "sunday": {"is_weekday": False, "activity": "sleeping in"},
}


@task(multiple_outputs=True)
def _going_to_the_beach() -> Dict:
    return {
        "subject": "Beach day!",
        "body": "It's Saturday and I'm heading to the beach.<br><br>Come join me!<br>",
    }

def _get_activity(day_name) -> str:
    activity_id = DAY_ACTIVITY_MAPPING[day_name]["activity"].replace(" ", "_")

    if DAY_ACTIVITY_MAPPING[day_name]["is_weekday"]:
        return f"weekday_activities.{activity_id}"

    return f"weekend_activities.{activity_id}"

@dag(
    start_date=datetime(2021, 6, 11),
    max_active_runs=1,
    schedule_interval="@daily",
    default_args={
        "owner": "community",
        "retries": 2,
        "retry_delay": timedelta(minutes=3),
    },
    default_view="graph",
    catchup=False,
    tags=["example"],
)
def example_dag_advanced():
    begin = DummyOperator(task_id="begin")
    end = DummyOperator(task_id="end", trigger_rule=TriggerRule.NONE_FAILED)

    # This task checks which day of the week it is
    check_day_of_week = BranchDayOfWeekOperator(
        task_id="check_day_of_week",
        week_day={WeekDay.SATURDAY, WeekDay.SUNDAY}, # This checks day of week
        follow_task_ids_if_true="weekend", # Next task if criteria is met
        follow_task_ids_if_false="weekday", # Next task if criteria is not met
        use_task_execution_day=True, # If True, uses task???s execution day to compare with is_today
    )

    weekend = DummyOperator(task_id="weekend") # "weekend" placeholder task
    weekday = DummyOperator(task_id="weekday") # "weekday" placeholder task

    # Templated value for determining the name of the day of week based on the start date of the DAG Run
    day_name = "{{ dag_run.start_date.strftime('%A').lower() }}"

    # Begin weekday tasks.
    # Tasks within this TaskGroup (weekday tasks) will be grouped together in the Airflow UI
    with TaskGroup("weekday_activities") as weekday_activities:
        which_weekday_activity_day = BranchPythonOperator(
            task_id="which_weekday_activity_day",
            python_callable=_get_activity, # Python function called when task executes
            op_args=[day_name],
        )

        for day, day_info in DAY_ACTIVITY_MAPPING.items():
            if day_info["is_weekday"]:
                day_of_week = Label(label=day)
                activity = day_info["activity"]

                # This task prints the weekday activity to bash
                do_activity = BashOperator(
                    task_id=activity.replace(" ", "_"),
                    bash_command=f"echo It's {day.capitalize()} and I'm busy with {activity}.", # This is the bash command to run
                )

                # Declaring task dependencies within the "TaskGroup" via the classic bitshift operator.
                which_weekday_activity_day >> day_of_week >> do_activity

    # Begin weekend tasks
    # Tasks within this TaskGroup will be grouped together in the UI
    with TaskGroup("weekend_activities") as weekend_activities:
        which_weekend_activity_day = BranchPythonOperator(
            task_id="which_weekend_activity_day",
            python_callable=_get_activity, # Python function called when task executes
            op_args=[day_name],
        )

        # Labels that will appear in the Graph view of the Airflow UI
        saturday = Label(label="saturday")
        sunday = Label(label="sunday")

        # This task prints the Sunday activity to bash
        sleeping_in = BashOperator(task_id="sleeping_in", bash_command="sleep $[ ( $RANDOM % 30 )  + 1 ]s")

        going_to_the_beach = _going_to_the_beach() # Calling the taskflow function

        # Because the "_going_to_the_beach()" function has "multiple_outputs" enabled, each dict key is
        # accessible as their own "XCom" key.
        inviting_friends = EmailOperator(
            task_id="inviting_friends",
            to="friends@community.com", # Email to send email to
            subject=going_to_the_beach["subject"], # Email subject
            html_content=going_to_the_beach["body"], # Eamil body content
        )

        # Using "chain()" here for list-to-list dependencies which are not supported by the bitshift
        # operator and to simplify the notation for the desired dependency structure.
        chain(which_weekend_activity_day, [saturday, sunday], [going_to_the_beach, sleeping_in])

    # High-level dependencies between tasks
    chain(begin, check_day_of_week, [weekday, weekend], [weekday_activities, weekend_activities], end)

    # Task dependency created by XComArgs:
    # going_to_the_beach >> inviting_friends

dag = example_dag_advanced()