/*---
thehive:
  name: assignToMe
  mode: Enabled
  definition: function_Action_assignToMe
  description: This function changes the assignee of the Case and all the associated tasks to the user who launches the function
  type: Action:Case
  vendor: Generic
  kind: function
  version: 1.0.0
---*/
function handle(input, context) {
    
    // Query to get the tasks of the case
    const query = [
        {
            "_name": "getCase",
            "idOrName": input._id
        },
        {
            "_name": "tasks"
        },
    ];
    
    // get the tasks
    const taskList = context.query.execute(query);
    
    // change the tasks assignee
    taskList.map((task) => {
        context.task.update(task._id, { assignee: context.userId })
    });
    
    // change the case assignee
    context.caze.update(input._id, { assignee: context.userId });
}