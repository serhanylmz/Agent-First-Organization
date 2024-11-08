# Config

Config files are the simple and recommended way to build your [TaskGraph](./TaskGraph.md). A standard JSON document, our generator can create and breakdown the role into a series of [Tasks](./Tasks.md) which are then matched with the appropriate agents and connected with the proper tasks to create a TaskGraph. 

Here is the structure for a *Config* JSON file:

* `role (Required)`: The general "role" of the chatbot you want to create
* `objective (Optional)`: The objective of the chatbot. This is like the "goal" or "target" you want your chatbot to fulfill or achieve while serving in its role.
* `domain (Optional)`: The domain of the company that you want to create the chatbot for
* `intro (Required)`: The introduction of the company that you want to create the chatbot for or the summary of the tasks that the chatbot need to handle
* `docs (Optional, Dict)`: The documents resources for the chatbot. The dictionary should contain the following fields:
    * `source (Required)`: The source url that you want the chatbot to refer to
    * `num (Required)`: The number of websites that you want the chatbot to refer to for the source
* `tasks (Optional, List(Dict))`: The pre-defined list of tasks that the chatbot need to handle. If empty, the system will generate the tasks and the steps to complete the tasks based on the role, objective, domain, intro and docs fields. The more information you provide in the fields, the more accurate the tasks and steps will be generated. If you provide the tasks, it should contain the following fields:
    * `task_name (Required, Str)`: The task that the chatbot need to handle
    * `steps (Required, List(Str))`: The steps to complete the task
* `agents (Required, List(AgentClassName))`: The [agents](./agents/agents.md) pre-defined under agentorg/agents folder that you want to use for the chatbot.

## Examples
#### [Customer Service Bot](./tutorials/customer-support.md)
```json title="customer_service_config.json"
{
    "role": "customer service assistant",
    "objective": [
        "Request customer contact information"
    ],
    "domain": "robotics and automation",
    "intro": "Richtech Robotics's headquarter is in Las Vegas; the other office is in Austin. Richtech Robotics provide worker robots (ADAM, ARM, ACE), delivery robots (Matradee, Matradee X, Matradee L, Richie), cleaning robots (DUST-E SX, DUST-E MX) and multipurpose robots (skylark). Their products are intended for business purposes, but not for home purpose; the ADAM robot is available for purchase and rental for multiple purposes. This robot bartender makes tea, coffee and cocktails. Richtech Robotics also operate the world's first robot milk tea shop, ClouTea, in Las Vegas (www.cloutea.com), where all milk tea beverages are prepared by the ADAM robot. The delivery time will be one month for the delivery robot, 2 weeks for standard ADAM, and two months for commercial cleaning robot. ",
    "docs": {
        "source": "https://www.richtechrobotics.com/",
        "num": 20
    },
    "tasks": [],
    "agents": [
        "RAGAgent",
        "RagMsgAgent",
        "MessageAgent",
        "SearchAgent",
        "DefaultAgent"
    ]
}
```