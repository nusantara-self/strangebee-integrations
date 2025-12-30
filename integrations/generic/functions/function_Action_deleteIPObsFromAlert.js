/*---
thehive:
  name: deleteIPObsFromAlert
  mode: Enabled
  definition: function_Action_deleteIPObsFromAlert
  description: This function will delete all the IP Observable from an alert
  type: Action:Alert
  vendor: Generic
  kind: function
  version: 1.0.0
---*/
function handle(input, context) {
    
    // Query to get the IP observables of the alert
    const query = [
        {
            "_name": "getAlert",
            "idOrName": input._id
        },
        {
            "_name": "observables"
        },
        {
            "_name": "filter",
            "_and":
            [
                {
                    "_field": "dataType",
                    "_value": "ip"
                }
            ]
        }
    ];
    
    // Get the IP observables of the alert
    const obsList = context.query.execute(query);
    
    // delete all the IP observables
    obsList.map((obs) => {
        context.observable.delete(obs._id);
      });

}