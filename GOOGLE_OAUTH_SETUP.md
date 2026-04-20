# Setting Up Google OAuth

## Step 1: Create Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the project dropdown at the top of the page.
3. Click on "New Project".
4. Enter the project name and click "Create".

## Step 2: Enable OAuth2 APIs
1. In the Google Cloud Console, navigate to the `API & Services` > `Library`.
2. Search for "Google+ API" and click on it.
3. Click on the "Enable" button. 
4. Repeat this for any other APIs you need for your application.

## Step 3: Create OAuth Credentials
1. Go to `API & Services` > `Credentials` in your Google Cloud Console.
2. Click on the "Create Credentials" button and select "OAuth Client ID".
3. If prompted, configure the consent screen by filling out the required fields.
4. Choose the application type (Web Application) and click "Create".
5. Note down the `Client ID` and `Client Secret` that are generated.

## Step 4: Configure Redirect URIs
1. In the credentials page, find the OAuth 2.0 Client IDs section.
2. Click on the name of the client ID you just created.
3. In the "Authorized redirect URIs" section, add the following URIs:
   - For localhost: `http://localhost:3000/auth/google/callback`
   - For production: `https://yourdomain.com/auth/google/callback`
4. Click "Save".

## Step 5: Copy Credentials to secrets.toml
1. Open your `secrets.toml` file in your project.
2. Add the following entries:
   ```toml
   [google]
   client_id = "YOUR_CLIENT_ID"
   client_secret = "YOUR_CLIENT_SECRET"
   ```
3. Replace `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` with the values you got from the Google Cloud Console.

## Step 6: Test Authentication Flow
1. Start your application.
2. Navigate to the login page that triggers Google authentication.
3. Click on the Google login button, and you should be redirected to the Google consent screen.
4. After granting permission, you should be redirected back to your application with an authenticated session.

## Additional Notes
- Ensure you have set up the correct scopes for the APIs you plan to use.
- Review the permissions requested in the consent screen to align with your application’s requirements.