/*---
thehive:
  name: assignAlert
  mode: Enabled
  definition: function_notifier_assignAlert
  description: This function is designed to trigger on alert creation event. It automatically assignes severity High & Critical alerts to a given user
  type: Notifier
  vendor: Generic
  kind: function
  version: 1.0.0
---*/
function handle(input, context) {
    // assignee for high & critical severity alerts. It has to be a valid TheHive login.
    const NewAssignee = 'userassignee@yourcompany.test';

    if (input.object.severity >= 3) {
        context.alert.update(input.object._id, { assignee: NewAssignee })
    };
}


