/*---
thehive:
  name: changeImportedAlertStatus
  mode: Enabled
  definition: function_notifier_changeImportedAlertStatus
  description: This function is designed to trigger on case closed event. It automatically changes imported alerts to a given custom status
  type: Notifier
  vendor: Generic
  kind: function
  version: 1.0.0
---*/
function handle(input, context) {
    // Query to get the LinkedAlerts
    const query = [
            {
              "_name" : "getCase",
              "idOrName": input.object._id
            },
            {
              "_name":"alerts"
            }
          ]
        
      // Get the linkedAlert list
      const alertList = context.query.execute(query);
      
      if (alertList.length > 0) {
        // change linked Alerts to ignore
        for (alert of alertList) {
          context.alert.update(alert._id, { "status": "Ignored", "stage": "Closed"})
        }
      }
}