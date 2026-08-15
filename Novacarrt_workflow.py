# Upgrade Databricks SDK to the latest version and restart Python to see updated packages
%pip install --upgrade databricks-sdk==0.70.0
%restart_python

from databricks.sdk.service.jobs import JobSettings as Job


NovaCart_workflow = Job.from_dict(
    {
        "name": "NovaCart_workflow",
        "email_notifications": {
            "on_success": [
                "charankumardamarla@gmail.com",
            ],
            "on_failure": [
                "charankumardamarla@gmail.com",
            ],
        },
        "tasks": [
            {
                "task_key": "Bronze",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/de.charan1610@gmail.com/Novacart/Bronze_layer_work",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Silver",
                "depends_on": [
                    {
                        "task_key": "Bronze",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/de.charan1610@gmail.com/Novacart/silver_layer_work",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Gold",
                "depends_on": [
                    {
                        "task_key": "Silver",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/de.charan1610@gmail.com/Novacart/gold_layer_work",
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "Dashboard",
                "depends_on": [
                    {
                        "task_key": "Gold",
                    },
                ],
                "dashboard_task": {
                    "subscription": {
                    },
                    "warehouse_id": "30cd675b382da7e7",
                    "dashboard_id": "01f1989a8cc81a94b208b82d4984bd0e",
                },
            },
            {
                "task_key": "Novacart_Alerts",
                "depends_on": [
                    {
                        "task_key": "Dashboard",
                    },
                ],
                "alert_task": {
                    "alert_id": "4436995847325089",
                    "warehouse_id": "30cd675b382da7e7",
                    "subscribers": [
                        {
                            "user_name": "de.charan1610@gmail.com",
                        },
                    ],
                },
            },
        ],
        "git_source": {
            "git_url": "https://github.com/charan1610/Novacart",
            "git_provider": "gitHub",
            "git_branch": "novacart_feature",
        },
        "queue": {
            "enabled": True,
        },
        "performance_target": "PERFORMANCE_OPTIMIZED",
    }
)

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
w.jobs.reset(new_settings=NovaCart_workflow, job_id=622790094791476)
# or create a new job using: w.jobs.create(**NovaCart_workflow.as_shallow_dict())
