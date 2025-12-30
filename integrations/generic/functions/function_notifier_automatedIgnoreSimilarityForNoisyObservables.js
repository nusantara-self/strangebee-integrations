/*---
thehive:
  name: automatedIgnoreSimilarityForNoisyObservables
  mode: Enabled
  definition: function_notifier_automatedIgnoreSimilarityForNoisyObservables
  description: This function is intended to be triggered on ObservableCreated events. It automatically sets ignoreSimilarity to true for observables matching a known list of common, noisy, or non-actionable values (such as localhost, private IPs, and generic hostnames..). This reduces alert noise and avoids false correlation in TheHive. Note that it is a workaround, and such issues are better managed in your alert ingestion pipeline(s)
  type: Notifier
  vendor: Generic
  kind: function
  version: 1.0.0
---*/
// Edit the BLOCKLIST below to suit your needs.

const BLOCKLIST = [
  "localhost",
  "127.0.0.1",
  "0.0.0.0",
  "::1",
  "255.255.255.255"
];

function handle(input, context) {
  var obs = input.object;
  var updated = false;

  // Making sure it is an observable
  if (obs && obs._type === "Observable" && obs._id && obs.data) {
    if (BLOCKLIST.indexOf(obs.data) !== -1) {
      context.observable.update(obs._id, { ignoreSimilarity: true });
      updated = true;
    }
  } else {
    // Not an observable, show the input for troubleshooting
    throw new Error("No valid observable in input: " + JSON.stringify(input));
  }
}
