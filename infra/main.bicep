param name string = 'skagent'
param location string = resourceGroup().location
param image string = 'ghcr.io/deinuser/skagent:latest'
param envVars object = {
  "AZURE_OPENAI_API_KEY": "..."
  "AZURE_OPENAI_ENDPOINT": "..."
}

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: name
  location: location
  properties: {
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
      }
      secrets: []
      environmentVariables: [
        for k in envVars: {
          name: k
          value: envVars[k]
        }
      ]
    }
    template: {
      containers: [
        {
          image: image
          name: name
        }
      ]
    }
  }
}
