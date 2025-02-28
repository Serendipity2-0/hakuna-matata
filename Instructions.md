# Typing Test Application Improvements

## New Features to Implement

### 1. User Selection
- Add user type selector dropdown
  - User Names :Chandana, Viju, Omkar, Snowy
  - Must select user before starting test
  - Disable selection during active test
  - Store selected user with test results

### 2. User Interface Components
- Add three difficulty levels: Easy, Medium, and Hard
- Each level should have different text lengths:
  - Easy: Create and use paragraph from a typingEasy.md
  - Medium: Create and use paragraph from a typingMedium.md
  - Hard: Create and use paragraph from a typingHard.md
- Add a difficulty selector dropdown
  - Use the Select component from UI components
  - Allow selection between Easy, Medium, and Hard
  - Disable selection during active test


### 3. Performance Metrics
- Implement accuracy calculation
  - Compare typed characters with sample text
  - Display accuracy percentage after test completion
- Display WPM (Words Per Minute) score
- Show both metrics in the results section

### 4. Result Management
- Add "Save Result" button
  - Appears after test completion
  - Stores results in DB\TypeNew.db database
- Display previous results history
  - Show WPM, accuracy, difficulty, and date
  - List in chronological order
