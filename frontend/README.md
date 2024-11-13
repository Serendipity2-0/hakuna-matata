This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

'Ctrl + H' to reset to home
'Ctrl + T' to open the Telegram message bubble
3. 'Esc' to close any open modal or the Telegram message bubble

## Rectangle Component Shortcuts

The application features four rectangle components that can be toggled using keyboard shortcuts:

- Ctrl/Cmd + W: Toggle the top rectangle
- Ctrl/Cmd + D: Toggle the right rectangle
- Ctrl/Cmd + S: Toggle the bottom rectangle
- Ctrl/Cmd + A: Toggle the left rectangle

Each rectangle occupies half the screen and slides in from its respective side when activated.

Note: Use Ctrl on Windows/Linux and Cmd (⌘) on Mac.



## Recent updates 





Claude 3.5 Sonnet (New)
Here's a detailed documentation based on the provided codebase:

# System Components Documentation

## 1. Home Page (HomeContent.tsx)
A modern, responsive landing page built with Next.js and Tailwind CSS.

### Core Components
- **Header Integration**: Seamless navigation header
- **Hero Section**: 
  ```tsx
  <h1 className="text-6xl md:text-7xl font-bold mb-8 max-w-4xl leading-tight">
      Documentation brings clarity to department
  </h1>

Copy

Apply

system-documentation.md
Value Proposition: Highlighted text with emphasis on processes, roles, and guidelines
Call-to-Action Buttons:
Primary: "Get Started" (Routes to registration)
Secondary: "Learn more" (Transparent design)
Technical Features
Client-side routing using Next.js Router
Responsive design breakpoints (md: 768px+)
Flex-based layout system
Dark theme implementation
2. Registration System (RegisterForm.tsx)
Advanced form handling with validation and API integration.

# Form Implementation
##  State Management:
const [formData, setFormData] = useState({
    email: '',
    department: '',
    phone_number: '',
    password: '',
    name: ''
});


# Validation Rules
Phone: 10-digit requirement with regex /^\d{10}$/
Required fields validation
Email format checking
API Integration
Endpoint: https://hakuna-matata.trademan.ai/register
Headers: Content-Type and Accept JSON
Response handling with status codes:
200: Success
409: Duplicate user
422: Invalid input
Department Mapping
const departmentMap = {
    'Serendipity': 1,
    'Trademan': 2,
    'DhoomStudios': 3
};



## 3. Navigation System (Header.tsx)
Clean and intuitive navigation interface.

# Components
   - Logo: Dynamic image loading with Next.js Image

# Navigation Links:
  - Showcase route
  - Login access


# Task Management
- Responsive Design: Hidden elements on mobile (md:flex)
Styling
- Consistent padding (p-6)
- Flex-based alignment
- Hover effects on interactive elements
- White background buttons with black text


# 4. Client-Side Features (ClientSideHome.tsx)
- Dynamic content rendering with advanced animations.

Animation Configuration
initial={{ opacity: 0 }}
animate={{ opacity: 1 }}
transition={{ duration: 0.5 }}



# Layout Features
- Gradient background (purple-400 to red-500)
- Centered content alignment
- Maximum width constraints
- Shadow effects
- Rounded corners
- Performance Optimizations
- Dynamic imports using Next.js dynamic
- SSR disabled for chat interface
- Spring animations for smooth transitions


# 5. Integration Architecture
- State Flow
- User interaction triggers
- Form submission handling
- API communication
- Response processing
- Navigation updates
- Error Handling Strategy
- Input validation
- API error catching
- Performance Considerations
- Lazy loading of components
- Optimized image loading
- Efficient state updates
- Responsive design principles


# 6. Development Guidelines
- Code Structure
- Component-based architecture
- Type safety with TypeScript
- Consistent styling with Tailwind
- Clear separation of concerns


# Best Practices
- Proper error handling
- User feedback mechanisms
- Performance optimization
- Responsive design implementation
- Clean code principles