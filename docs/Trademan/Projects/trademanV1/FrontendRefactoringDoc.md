# Refactaring of frontend trademan v1 react

[TradeMan](https://trademan.ai/)

## 1. Refactoring main/Logo.tsx

- Documetation

In-depth technical documentation outline and detailed documentation for the refactoring process you completed for the `Logo.tsx` component.

---

## 2. Documentation: Refactoring `Logo.tsx` Component

### 2.1 Overview

The `Logo.tsx` component in our application displays clickable logo letters, heart icons, and a login dialog box. This documentation covers the recent refactoring process, focusing on adding required `width` and `height` properties to `Image` components, organizing constants, and improving maintainability. The goal is to make the component more flexible, maintainable, and easy to understand.

### 2.2 Introduction to Refactoring

#### 2.2.1 Purpose of Refactoring

The purpose of this refactor is to enhance the maintainability, flexibility, and readability of the `Logo.tsx` component by:

- Organizing constants, routes, and image paths in a separate file.
- Ensuring that each `Image` component has required properties, such as `width` and `height`, to avoid rendering errors.
- Removing hardcoded values, allowing for easier updates in the future.

#### 2.2.2 Objectives of This Refactor

- **Resolve Issues**: Address missing `width` and `height` properties in `Image` components to ensure proper rendering.
- **Increase Customization**: Centralize constants for easy access and modification.
- **Enhance Readability and Maintainability**: Organize code to make the component easier to understand and maintain over time.

---

### 2.3 Refactoring Breakdown

#### 2.3.1 Step1 : Organizing Constants

All hardcoded values, such as image paths, routes, and action sequences, were moved into a dedicated `constants.ts` file. This change improves maintainability by allowing updates in one location without modifying the component code.

#### 2.3.1 Step2 : Adding Required Properties to Image Components

To resolve rendering issues, `width` and `height` properties were added to each `Image` component. This ensures that each image has a consistent size, reducing potential layout shifts.

#### 2.3.1 Step3: Ensuring Maintainability and Customization

Hardcoded values for image paths, click sequences, and routes were replaced with constants, making the code modular, reusable, and easy to modify. Each section of the component now refers to values in `constants.ts`, increasing flexibility and customization.

---

### 2.4 Detailed Refactoring Process

#### 2.4.1 Initial Code Analysis

**Issues Identified**:

- Missing `width` and `height` properties for `Image` components, causing rendering warnings.
- Hardcoded values (e.g., image paths, sequences, routes) scattered throughout the code, reducing readability and increasing maintenance time.

#### 2.4.2 Refactored Code Structure

The refactored code is organized as follows:

1. **Constants** are defined in a separate file (`constants.ts`).
2. **Image Properties** (`width` and `height`) are explicitly set to avoid warnings.
3. **Functionality** remains the same, but the organization improves readability and modularity.

#### 2.4.3 Explanation of Each Refactored Section

**Constants File (`constants.ts`)**

This file holds the following constants:

- `IMAGE_PATHS`: Contains paths to all images used in `Logo.tsx`.
- `LOGO_SEQUENCES`: Defines click sequences for different actions (e.g., registration, profile, admin).
- `ROUTES`: Contains routes for navigation.
- `CLICKABLE_LETTERS`: Defines letters that should respond to clicks.
- **Example**:

            tsx

            // constants.ts
            export const IMAGE_PATHS = {
                T: "/images/T.png",
                R: "/images/R.png",
                ...
                greenHeart: "/images/GreenHeart.png",
                redHeart: "/images/RedHeart.png",
                backgroundImage: "/images/circleImg.png",
            };
            export const LOGO_SEQUENCES = { register: "TRNAME", profile: "NARTME", admin: "REDMAN" };
            export const ROUTES = { register: "/register", profile: "/user-profile", admin: "/admin" };
            export const CLICKABLE_LETTERS = ["T", "R", "A", "N", "D", "E", "M"];




  **Refactored `Logo.tsx`**

  - **Image Properties**: Each `Image` component now has `width` and `height` properties, ensuring that all images render correctly.
  - **Constants Usage**: The component imports constants from `constants.ts`, removing hardcoded values and improving modularity.
  - **Example** (refactored `Image`):

          tsx

          <Image
              src={IMAGE_PATHS.T}
              alt="T"
              width={100}
              height={100}
              onClick={() => handleClick("T")}
              className={`cursor-pointer duration-300 w-[70px] h-[70px] md:w-[100px] md:h-[100px] ${clickedText.includes("T") && "hover:scale-75"}`}
          />


---

### 2.5. Testing the Refactor

#### 2.5.1 Testing Methods

Testing was conducted by verifying:

1. **Image Rendering**: Ensuring each `Image` displays with correct dimensions.
2. **Functionality**: Checking that all routes, sequences, and clicks behave as expected.
3. **Responsiveness**: Confirming that the component layout adapts well to different screen sizes.

#### 2.5.2 Expected Behavior After Refactor

- No warnings about missing `width` and `height` properties for `Image` components.
- Consistent behavior with defined sequences triggering the correct routes.
- Component should be easy to update without directly modifying `Logo.tsx`.

---

### 2.6 Best Practices Applied

#### 2.6.1 Modularization and Reusability

The refactor centralized hardcoded values in `constants.ts`, allowing reuse across the component without duplicating values.

#### 2.6.2 Avoiding Hardcoded Values

Replacing inline hardcoded values with constants improves readability, maintainability, and flexibility.

#### 2.6.3 Component Flexibility

This refactor allows developers to easily add or change images, routes, or click sequences by updating `constants.ts` rather than editing the component code.

---

### 2.7. Future Recommendations

#### 2.7.1 Additional Improvements

1. **Prop-Driven Configuration**: Consider making the component accept props for routes, images, and sequences, allowing different configurations.
2. **Unit Testing**: Add unit tests to ensure functionality remains consistent through future updates.

#### 2.7.2 Suggested Enhancements

- **Dynamic Image Sizing**: Make image dimensions configurable based on screen size.
- **User Feedback**: Add tooltips or visual indicators for each clickable letter for better UX.

---

## 3. Conclusion

The `Logo.tsx` refactor successfully enhances the component by:

- Adding required image properties,
- Centralizing constants, and
- Improving modularity and flexibility.

By following this documentation, future developers can easily understand and extend the `Logo.tsx` component, ensuring maintainability and consistent functionality.
