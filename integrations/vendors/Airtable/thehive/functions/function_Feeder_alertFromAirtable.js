/*---
thehive:
  name: alertFromAirtable
  mode: Enabled
  definition: function_Feeder_alertFromAirtable
  description: This function creates alerts from data coming from a Airtable database. It checks the alert does not already exist, then creates the alert, and completes type, source, source-ref, title, description and tags
  type: Feeder
  vendor: Airtable
  kind: function
  version: 1.0.0
---*/
function handle(input, context) {
    const issues = input.records;
    issues.map((issue) => {

      // check if the alert already exists
      const filters = [
        {
          _name: "filter",
          _and: [
            { 
              _field: "sourceRef", 
              _value: issue.id 
            }
          ]
        }
      ];
      if (context.alert.find(filters).length < 1) {
        // the Alert does not exist in TheHive yet, we create it
        const desc = issue.fields["Issue Description"]
        const alert = {
          "type": "event",
          "source": "Feeder-Airtable",
          "sourceRef": issue.id,
          "title": "Incident reported: " + issue.fields["Incident Category"] + " - " + issue.fields["Department"],
          "description": desc,
          "tags": ['Alertfeeder', 'Airtable', issue.fields["Incident Category"]]
        };
        context.alert.create(alert);
      }
    });
}