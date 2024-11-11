// // src/components/Header.tsx

// import Link from 'next/link';
// import Image from 'next/image';
// import React from 'react';

// const Header: React.FC = () => {
//     return (
//         <header className="w-full p-6 flex justify-between items-center">
//             <div className="flex items-center space-x-6">
//                 <div className="flex items-center space-x-2">
//                     <Link href="/">
//                         <Image
//                             src="/logo.png"
//                             alt="Serendipity Logo"
//                             width={48}
//                             height={48}
//                             className="object-contain rounded-full"
//                             priority
//                         />
//                     </Link>
//                 </div>
//                 <nav className="hidden md:flex space-x-6 text-sm">
//                     <Link href="/showcase" className="text-gray-400 text-2xl hover:text-white">Serendipity</Link>
//                 </nav>
//             </div>

//             <div className="flex items-center space-x-4">
//                 <Link
//                     href="/login"
//                     className="bg-white text-black px-4 py-2 rounded-lg text-sm hover:bg-gray-100"
//                 >
//                     Login
//                 </Link>

//                 {/* <Link
//                     href="/"
//                     className="bg-white text-black px-4 py-2 rounded-lg text-sm hover:bg-gray-100"
//                 >
//                     Serendipity Task Management 
//                 </Link> */}

//                 {/* <ClientSideHome /> */}

//             </div>
//         </header>
//     );
// };

// export default Header;


// // src/components/Header.tsx

// import Link from 'next/link';
// import Image from 'next/image';
// import React, { useState } from 'react';
// import dynamic from 'next/dynamic';

// // Dynamically import ClientSideHome with no server-side rendering
// const ClientSideHome = dynamic(() => import('./ClientSideHome'), { ssr: false });

// const Header: React.FC = () => {
//     const [showClientSideHome, setShowClientSideHome] = useState(false);

//     const toggleClientSideHome = () => {
//         setShowClientSideHome(!showClientSideHome);
//     };

//     return (
//         <header className="w-full p-6 flex justify-between items-center">
//             <div className="flex items-center space-x-6">
//                 <div className="flex items-center space-x-2">
//                     <Link href="/">
//                         <Image
//                             src="/logo.png"
//                             alt="Serendipity Logo"
//                             width={48}
//                             height={48}
//                             className="object-contain rounded-full"
//                             priority
//                         />
//                     </Link>
//                 </div>
//                 <nav className="hidden md:flex space-x-6 text-sm">
//                     <Link href="/showcase" className="text-gray-400 text-2xl hover:text-white">Serendipity</Link>
//                 </nav>
//             </div>

//             <div className="flex items-center space-x-4">
//                 <Link
//                     href="/login"
//                     className="bg-white text-black px-4 py-2 rounded-lg text-sm hover:bg-gray-100"
//                 >
//                     Login
//                 </Link>

//                 <button
//                     onClick={toggleClientSideHome}
//                     className="bg-white text-black px-4 py-2 rounded-lg text-sm hover:bg-gray-100"
//                 >
//                     Serendipity Task Management
//                 </button>

//                 {/* Conditionally render ClientSideHome as a modal or dropdown */}
//                 {showClientSideHome && (
//                     <div className="absolute top-16 right-0 mt-4 w-full max-w-md p-6 bg-white rounded-lg shadow-lg z-50">
//                         <button
//                             onClick={toggleClientSideHome}
//                             className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
//                         >
//                             ✕
//                         </button>
//                         <ClientSideHome />
//                     </div>
//                 )}
//             </div>
//         </header>
//     );
// };

// export default Header;
// src/components/Header.tsx

import Link from 'next/link';
import Image from 'next/image';
import React from 'react';

const Header: React.FC = () => {
    return (
        <header className="w-full p-6 flex justify-between items-center">
            <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                    <Link href="/">
                        <Image
                            src="/logo.png"
                            alt="Serendipity Logo"
                            width={48}
                            height={48}
                            className="object-contain rounded-full"
                            priority
                        />
                    </Link>
                </div>
                <nav className="hidden md:flex space-x-6 text-sm">
                    <Link href="/showcase" className="text-gray-400 text-2xl hover:text-white">Serendipity</Link>
                </nav>
            </div>

            <div className="flex items-center space-x-4">
                <Link
                    href="/login"
                    className="bg-white text-black px-4 py-2 rounded-lg text-sm hover:bg-gray-100"
                >
                    Login
                </Link>

                <Link
                    href="/client-side-home" // Link to the new page
                    className="bg-white text-black px-4 py-2 rounded-lg text-sm hover:bg-gray-100"
                >
                    Serendipity Task Management
                </Link>
            </div>
        </header>
    );
};

export default Header;
