# Azure Functions
## Process files and blobs - create an image thumbnail (Python)
This sample demonstrates how to take image files as an input via BlobTrigger, transform the file to create a thumbnail, and then output the new file as a blob via BlobOutput binding.

## Run on your local environment
### Pre-reqs for local development
1. Python xx or higher
2. Azure Functions Core Tools
3. Add this `local.settings.json`` file to your /files/dotnet folder to simplify local development using azurite (storage emulator).
