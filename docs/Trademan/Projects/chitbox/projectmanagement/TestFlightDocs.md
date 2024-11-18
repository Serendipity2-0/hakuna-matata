# Test flight documentation

Creating and managing TestFlight builds for your app in the Apple Developer Console involves several detailed steps. Here’s a comprehensive guide to help you through the process:

### Step-by-Step Guide to Create TestFlight Builds for iOS Apps

### Prerequisites:

- An Apple Developer account
- A macOS device with Xcode installed
- Your app’s project ready in Xcode

### Step 1: Prepare Your App in Xcode

1. **Open Your Project:**
    - Open your app project in Xcode.
2. **Update App Version and Build Number:**
    - Navigate to the project settings.
    - Increment the version and build number in the “General” tab under the "Identity" section.
3. **Select Your Development Team:**
    - Under the “Signing & Capabilities” tab, ensure you have selected your Apple Developer team.
4. **Archive Your App:**
    - Select a generic iOS device or Any iOS Device (arm64) from the device selection menu.
    - Go to `Product` > `Archive` to create an archive of your app.

### Step 2: Upload Your Build to App Store Connect

1. **Open the Organizer:**
    - After the archive is created, the Organizer window will open. If it doesn’t, you can open it via `Window` > `Organizer`.
2. **Distribute Your App:**
    - Select the archive and click on the `Distribute App` button.
    - Choose `App Store Connect` as the distribution method.
    - Select `Upload` as the destination.
3. **Select Options:**
    - Follow the prompts to choose the appropriate options, such as including bitcode, enabling symbolication, etc.
4. **Upload the Build:**
    - Xcode will validate the build and then upload it to App Store Connect. You’ll receive a confirmation once the upload is successful.

### Step 3: Configure Your App in App Store Connect

1. **Log in to App Store Connect:**
    - Visit [App Store Connect](https://appstoreconnect.apple.com/) and log in with your Apple Developer account.
2. **Select Your App:**
    - Go to the `My Apps` section and select the app you uploaded.
3. **Add a New Build:**
    - In the `App Store` tab, click on `TestFlight`.
    - Under `Builds`, click on the `+` button to add a new build.
4. **Choose the Build:**
    - Select the build you just uploaded and click `Done`.

### Step 4: Set Up Internal Testing

1. **Add Internal Testers:**
    - In the `TestFlight` tab, navigate to `Internal Testing`.
    - Click on the `+` button to add internal testers (usually team members).
2. **Invite Testers:**
    - Select team members from the list and send invitations.

### Step 5: Set Up External Testing

1. **Add a New Group:**
    - Navigate to the `External Testing` section.
    - Create a new group and add external testers (email addresses required).
2. **Submit for Beta App Review:**
    - Before external testers can use TestFlight, Apple needs to review the build.
    - Provide the necessary information for review, including test details and any specific testing instructions.
3. **Wait for Review Approval:**
    - Apple will review your submission. Once approved, you can invite external testers.

### Step 6: Manage TestFlight Builds

1. **Send Invitations:**
    - Once the build is approved, send invitations to external testers through the TestFlight interface.
2. **Monitor Testing:**
    - Use the TestFlight dashboard to monitor tester feedback, crashes, and sessions.
3. **Update Builds:**
    - Repeat the steps to upload new builds as needed. Testers will receive updates automatically via the TestFlight app.

### Additional Tips

- **Beta Information:**
    - Ensure you provide clear testing instructions and a contact email for feedback.
- **TestFlight App:**
    - Testers will need to install the TestFlight app from the App Store to test your app.
- **Feedback:**
    - Encourage testers to provide detailed feedback and report any issues they encounter.

By following these detailed steps, you can effectively manage and distribute your app builds using TestFlight, ensuring a smooth beta testing process for your iOS app.

[Link](https://developer.apple.com/programs/enroll/)