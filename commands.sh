# Script to deploy the FlaskSklearn App to Azure App Service using Azure CLI

# Set variables
APP_NAME="flasksklearn-app"
RESOURCE_GROUP="Azuredevops"
LOCATION="southcentralus"
SKU="B1"

# Deploy the web app
az webapp up -n $APP_NAME --resource-group $RESOURCE_GROUP --location $LOCATION --sku $SKU

# Display app details
az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP

# Enable logging
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP