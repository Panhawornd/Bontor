"use client";

import { useState, useEffect, useRef, useLayoutEffect } from "react";
import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";
import {
  User,
  LogOut,
  ChevronDown,
  Edit,
  Search,
  Paperclip,
  ArrowUp,
  Bot,
  Trash2,
} from "lucide-react";

export default function AgentPage() {
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [hasToken, setHasToken] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<{ name: string; email?: string } | null>(
    null
  );
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef<HTMLDivElement>(null);
  const [chatHistory, setChatHistory] = useState<{ title: string; messages: { role: 'user' | 'assistant'; content: string }[] }[]>([]);
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [activeChatIndex, setActiveChatIndex] = useState<number | null>(null);
  const chatAreaRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const inputContainerRef = useRef<HTMLDivElement>(null);
  const [inputHeight, setInputHeight] = useState(100); // Default bottom padding
  const hasLoaded = useRef(false); // Prevent save effect from overwriting on initial mount

  // Load chat history and active chat index from localStorage on component mount
  useEffect(() => {
    const savedChatHistory = localStorage.getItem('chatHistory');
    const savedActiveChatIndex = localStorage.getItem('activeChatIndex');
    
    if (savedChatHistory) {
      try {
        const parsedHistory = JSON.parse(savedChatHistory);
        // Filter out chats with no messages
        const filteredHistory = parsedHistory.filter((chat: { title: string; messages: { role: 'user' | 'assistant'; content: string }[] }) => chat.messages && chat.messages.length > 0);
        setChatHistory(filteredHistory);
        
        // If we have a saved active chat index and it's valid, load those messages
        if (savedActiveChatIndex !== null) {
          const activeIndex = parseInt(savedActiveChatIndex);
          if (!isNaN(activeIndex) && activeIndex >= 0 && activeIndex < filteredHistory.length) {
            setActiveChatIndex(activeIndex);
            setMessages(filteredHistory[activeIndex].messages);
          }
        }
      } catch (error) {
        console.error('Error loading chat history:', error);
      }
    }
    hasLoaded.current = true;
  }, []);

  // Save chat history to localStorage whenever it changes
  useEffect(() => {
    if (!hasLoaded.current) return; // Skip save until load has completed
    // Filter out chats with no messages before saving
    const filteredHistory = chatHistory.filter(chat => chat.messages && chat.messages.length > 0);
    localStorage.setItem('chatHistory', JSON.stringify(filteredHistory));
  }, [chatHistory]);

  // Save active chat index to localStorage whenever it changes
  useEffect(() => {
    if (activeChatIndex !== null) {
      localStorage.setItem('activeChatIndex', activeChatIndex.toString());
    } else {
      localStorage.removeItem('activeChatIndex');
    }
  }, [activeChatIndex]);

  useEffect(() => {
    // Check if user is authenticated via cookie
    const checkAuth = async () => {
      try {
        const response = await fetch("/api/auth/me");
        const data = await response.json();

        if (data.user) {
          setUser(data.user);
          setHasToken(true);
        } else {
          setHasToken(false);
        }
      } catch (error) {
        console.error("Auth check error:", error);
        setHasToken(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Close profile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        profileMenuRef.current &&
        !profileMenuRef.current.contains(event.target as Node)
      ) {
        setShowProfileMenu(false);
      }
    };

    if (showProfileMenu) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showProfileMenu]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [messages]);

  // Auto-resize textarea and update bottom padding
  useLayoutEffect(() => {
    if (textareaRef.current) {
      // Reset height to auto to get the correct scrollHeight
      textareaRef.current.style.height = 'auto';
      
      const scrollHeight = textareaRef.current.scrollHeight;
      // Enforce min height of 60px (matching the CSS min-h-[60px])
      const newHeight = Math.max(scrollHeight, 60);
      
      textareaRef.current.style.height = `${Math.min(newHeight, 200)}px`;
    }

    // Measure input container height to adjust chat padding
    if (inputContainerRef.current) {
      // Add a small buffer (e.g., 20px)
      setInputHeight(inputContainerRef.current.offsetHeight + 20);
    }
  }, [inputValue]);
  
  const getMockResponse = (userMessage: string) => {
    const lowerMessage = userMessage.toLowerCase();
    if (lowerMessage.includes('software engineering')) {
      return `Software Engineering is the application of engineering principles to software development. It involves designing, developing, testing, and maintaining software systems.

Fundamental skills to prepare before enrolling:
- Programming languages: Python, Java, C++
- Data structures and algorithms
- Version control (Git)
- Problem-solving and logical thinking
- Basic understanding of databases and web development`;
    } else if (lowerMessage.includes('data science')) {
      return `Data Science combines statistics, programming, and domain expertise to extract insights from data. It involves collecting, processing, and analyzing large datasets to inform decision-making.

Fundamental skills to prepare before enrolling:
- Programming: Python or R
- Statistics and mathematics
- Data manipulation (Pandas, SQL)
- Machine learning basics
- Data visualization (Matplotlib, Tableau)`;
    } else if (lowerMessage.includes('telecom') || lowerMessage.includes('networking')) {
      return `Telecommunications and Networking involves the transmission of information over distances using electronic means. It covers network design, protocols, and infrastructure for data, voice, and video communication.

Fundamental skills to prepare before enrolling:
- Computer networking basics (TCP/IP, OSI model)
- Programming: Python or Java
- Understanding of network security
- Knowledge of wireless technologies
- Basic electronics and signal processing`;
    } else if (lowerMessage.includes('cybersecurity') || lowerMessage.includes('cyber security')) {
      return `Cybersecurity focuses on protecting systems, networks, and data from digital attacks. It involves implementing security measures to prevent unauthorized access, data breaches, and cyber threats.

Fundamental skills to prepare before enrolling:
- Networking fundamentals
- Programming: Python, Bash scripting
- Understanding of encryption and cryptography
- Knowledge of operating systems (Linux, Windows)
- Ethical hacking and penetration testing basics`;
    } else {
      return `I'm here to help with information about majors and skills to prepare. Please ask about one of these areas for specific details and preparation skills!`;
    }
  };

  const handleSend = () => {
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = { role: 'user' as const, content: inputValue };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');

    // Reset textarea height if possible (since we can't easily access the ref here without passing it or using a ref for the textarea)
    // But since inputValue controls the value, the next render will clear the text.
    // The height reset is handled by the useEffect on inputValue or the style prop.
    
    // Handle chat history update — capture the resolved index for the timeout below
    let resolvedIndex: number;
    if (activeChatIndex === null) {
      // No active chat (deleted or fresh start) — create a new one
      const newChatTitle = `Chat ${chatHistory.length + 1}`;
      const newChat = { title: newChatTitle, messages: newMessages };
      resolvedIndex = chatHistory.length;
      setChatHistory(prev => [...prev, newChat]);
      setActiveChatIndex(resolvedIndex);
    } else {
      resolvedIndex = activeChatIndex;
      // Update existing active chat
      setChatHistory(prev => {
        const updatedHistory = [...prev];
        if (updatedHistory[resolvedIndex]) {
          updatedHistory[resolvedIndex].messages = newMessages;
        }
        return updatedHistory;
      });
    }

    // Simulate assistant response after 1 second
    setTimeout(() => {
      const responseContent = getMockResponse(userMessage.content);
      const assistantMessage = { role: 'assistant' as const, content: responseContent };
      const finalMessages = [...newMessages, assistantMessage];
      setMessages(finalMessages);

      // Update chat history with assistant response
      setChatHistory(prev => {
        const updatedHistory = [...prev];
        if (updatedHistory[resolvedIndex]) {
          updatedHistory[resolvedIndex].messages = finalMessages;
        }
        return updatedHistory;
      });
    }, 1000);
  };

  const handleNewChat = () => {
    // Don't create new chat if there are no chats yet
    if (chatHistory.length === 0) return;

    // Save current messages to the active chat in history if it exists and has messages
    if (messages.length > 0 && activeChatIndex !== null) {
      setChatHistory(prev => {
        const updatedHistory = [...prev];
        if (updatedHistory[activeChatIndex]) {
          updatedHistory[activeChatIndex].messages = messages;
        }
        return updatedHistory;
      });
    }

    // Start new chat
    setMessages([]);
    const newChatIndex = chatHistory.length;
    setChatHistory(prev => [...prev, { title: `Chat ${prev.length + 1}`, messages: [] }]);
    setActiveChatIndex(newChatIndex);
  };

  const handleLoadChat = (chatIndex: number) => {
    const selectedChat = chatHistory[chatIndex];
    if (selectedChat) {
      setMessages(selectedChat.messages);
      setActiveChatIndex(chatIndex);
    }
  };

  const handleDeleteChat = (chatIndex: number, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent triggering the load chat function
    
    setChatHistory(prev => {
      const updatedHistory = prev.filter((_, idx) => idx !== chatIndex);
      
      // If we deleted the currently active chat, clear messages and reset active index
      if (activeChatIndex === chatIndex) {
        setMessages([]);
        setActiveChatIndex(null);
      } else if (activeChatIndex !== null && activeChatIndex > chatIndex) {
        // If we deleted a chat before the active one, adjust the active index
        setActiveChatIndex(activeChatIndex - 1);
      }
      
      return updatedHistory;
    });
  };

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    localStorage.setItem('just_logged_out', 'true');
    localStorage.removeItem('just_logged_in');
    window.location.href = "/landing";
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        padding: '40px 20px',
        position: 'relative'
      }}>
        {/* Ultravib image background */}
        <div
          style={{ 
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundImage: "url(/image/Ultravib.png)",
            backgroundSize: 'cover',
            backgroundPosition: 'center center',
            backgroundRepeat: 'no-repeat',
            filter: 'brightness(0.9)',
            zIndex: 0,
            pointerEvents: 'none'
          }}
        />
        <div style={{ position: 'relative', zIndex: 10 }}>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '24px'
          }}>
            <svg className="logo-spin" width="80" height="80" viewBox="-30 -30 201 233" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ display: 'block' }}>
              <g>
                <path d="M110.464 0C127.032 0.000247877 140.464 13.4316 140.464 30V31.4922H92.9033V58.2891H49.9043V86.3154H0V30C0 13.4315 13.4315 1.61637e-06 30 0H110.464Z" fill="white"/>
              </g>
              <g>
                <path d="M30.5372 172.649C13.9687 172.67 0.453776 159.257 0.350835 142.689L0.341564 141.196L47.9011 141.134L47.7346 114.338L90.7336 114.282L90.5595 86.2549L140.464 86.1897L140.814 142.505C140.917 159.073 127.569 172.522 111 172.544L30.5372 172.649Z" fill="#3B82F6"/>
              </g>
            </svg>
            <img 
              src="/image/Bontor-logo.png" 
              alt="Bontor" 
              style={{ 
                height: '30px',
                width: 'auto',
                display: 'block'
              }}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen overflow-hidden text-white relative bg-black">
      {/* Ultravib image background with dark overlay */}
      <div
        className="fixed inset-0"
        style={{
          backgroundImage: "url(/image/Ultravib.png)",
          backgroundSize: "cover",
          backgroundPosition: "center center",
          backgroundRepeat: "no-repeat",
          filter: "brightness(0.9)",
          zIndex: 0,
          pointerEvents: "none",
        }}
      />

      {/* Header */}
      <header
        className="bg-white/2 backdrop-blur-md flex-shrink-0 relative z-50"
        style={{
          padding: "16px 0",
          minHeight: "4rem",
        }}
      >
        <div
          className="max-w-[1200px] 2xl:max-w-none mx-auto px-6 2xl:px-24 h-full"
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "auto 1fr auto",
              alignItems: "center",
              height: '100%',
              position: 'relative'
            }}
          >
            {/* Logo and mobile menu */}
            <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <button
                onClick={() => setIsMenuOpen(true)}
                className="lg:hidden p-2 hover:bg-gray-800 rounded-md transition-colors"
                style={{ background: 'transparent', border: 'none' }}
                aria-label="Open menu"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 22 22"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M21 5H3" />
                  <path d="M21 12H9" />
                  <path d="M21 19H7" />
                </svg>
              </button>
              <button
                onClick={() => router.push("/landing")}
                className="hover:opacity-80 transition-opacity"
                style={{
                  background: "transparent",
                  border: "none",
                  padding: 0,
                }}
              >
                <img
                  src="/image/Bontor-logo.png"
                  alt="Bontor"
                  className="h-5 md:h-[23px] w-auto"
                />
              </button>
            </div>

            {/* Navigation Links - Centered - Hidden on mobile */}
            <div
              className="hidden lg:flex items-center space-x-8"
              style={{ position: "absolute", left: "50%", transform: "translateX(-50%)" }}
            >
              <button
                onClick={() => router.push("/Input")}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Analyze
              </button>
              <button
                onClick={() => router.push("/dashboard")}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Dashboard
              </button>
              <button
                onClick={() => router.push("/university")}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                University
              </button>
              <button
                onClick={() => router.push("/agent")}
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Agent
              </button>
            </div>

            {/* Profile Menu */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifySelf: "end",
                gap: "8px",
                position: "relative",
              }}
            >
              <div ref={profileMenuRef} style={{ position: "relative" }}>
                <button
                  onClick={() => setShowProfileMenu(!showProfileMenu)}
                  className="flex items-center gap-2 px-3 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
                  style={{
                    fontSize: "14px",
                  }}
                >
                  <User size={16} />
                  <span className="hidden sm:inline max-w-[120px] truncate">
                    {user?.name ?? '\u00A0'}
                  </span>
                  <ChevronDown
                    size={14}
                    style={{
                      transform: showProfileMenu
                        ? "rotate(180deg)"
                        : "rotate(0deg)",
                      transition: "transform 0.2s",
                    }}
                  />
                </button>

                {/* Dropdown Menu */}
                {showProfileMenu && (
                  <div
                    style={{
                      position: "absolute",
                      top: "100%",
                      right: 0,
                      marginTop: "8px",
                      background: "#1f2937",
                      border: "1px solid #374151",
                      borderRadius: "8px",
                      minWidth: "160px",
                      boxShadow: "0 10px 25px rgba(0, 0, 0, 0.5)",
                      zIndex: 1000,
                      overflow: "hidden",
                    }}
                  >
                    <div
                      style={{
                        padding: "8px 12px",
                        borderBottom: "1px solid #374151",
                      }}
                    >
                      <p
                        style={{
                          color: "#ffffff",
                          fontSize: "14px",
                          fontWeight: "600",
                          margin: 0,
                        }}
                      >
                        {user?.name || "User"}
                      </p>
                      {user?.email && (
                        <p
                          style={{
                            color: "#9ca3af",
                            fontSize: "12px",
                            margin: "4px 0 0 0",
                          }}
                        >
                          {user.email}
                        </p>
                      )}
                    </div>
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-4 py-3 text-white hover:bg-gray-700 transition-colors"
                      style={{
                        fontSize: "14px",
                        background: "transparent",
                        border: "none",
                        cursor: "pointer",
                        textAlign: "left",
                      }}
                    >
                      <LogOut size={16} />
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Sidebar Menu */}
      {isMenuOpen && (
        <div className="fixed inset-0 z-[200] lg:hidden">
          <button
            className="absolute inset-0 bg-black/60 backdrop-blur-md"
            aria-label="Close menu"
            onClick={() => setIsMenuOpen(false)}
          />
          <aside
            className="absolute top-0 left-0 h-full w-72 max-w-[80%] text-white border-r border-white/10 shadow-2xl"
            style={{
              backgroundImage:
                "linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url(/image/Ultravib.png)",
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          >
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
              <span className="text-base font-semibold tracking-wide uppercase">
                Menu
              </span>
              <button
                onClick={() => setIsMenuOpen(false)}
                className="p-1 text-white/80 hover:text-white transition-colors"
                aria-label="Close menu"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  width="24"
                  height="24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
            <div className="flex flex-col gap-6 px-5 py-6 text-sm">
              <button
                onClick={() => { router.push('/Input'); setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Analyze
              </button>
              <button
                onClick={() => { router.push('/dashboard'); setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Dashboard
              </button>
              <button
                onClick={() => { router.push('/university'); setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                University
              </button>
              <button
                onClick={() => { router.push('/agent'); setIsMenuOpen(false); }}
                className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors"
              >
                Agent
              </button>
            </div>
            <div className="mt-5 px-5 pb-8">
              <div className="mb-3">
                <p className="text-white font-semibold text-sm">{user?.name}</p>
                {user?.email && (
                  <p className="text-white/60 text-xs mt-1">{user.email}</p>
                )}
              </div>
              <button
                onClick={() => { handleLogout(); setIsMenuOpen(false); }}
                className="w-full justify-center px-4 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
              >
                Logout
              </button>
            </div>
          </aside>
        </div>
      )}

      {/* Main content area */}
      <div className="relative z-10 flex flex-1 overflow-hidden">
        {/* Sidebar for chat history */}
        <aside className="hidden md:flex flex-col w-64 flex-shrink-0 bg-[#111111] border-r border-[#1f1f1f] overflow-y-auto z-20">
          <div className="p-4">
            <button
              type="button"
              onClick={handleNewChat}
              className="w-full flex items-center gap-3 px-2 py-2 rounded-md hover:bg-white/5 transition-colors text-gray-100"
            >
              <Edit className="w-4 h-4" />
              <span className="text-sm text-white">New chat</span>
            </button>

            <button
              type="button"
              className="w-full flex items-center gap-3 px-2 py-2 mt-2 rounded-md hover:bg-white/5 transition-colors text-gray-100"
            >
              <Search className="w-4 h-4" />
              <span className="text-sm text-white">Search chats</span>
            </button>

            <div className="mt-4 border-t border-gray-700 pt-3 px-2">
              <p className="text-xs text-gray-400 uppercase tracking-wide">Chat history</p>

              {chatHistory.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-8 px-2 text-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
                  </svg>
                  <p className="text-sm text-gray-200 font-semibold">No chats yet</p>
                  <p className="text-xs text-gray-400 mt-2">Start a new chat to see it here.</p>
                </div>
              ) : (
                <div>
                  {/* Chat items */}
                  {chatHistory.map((c, idx) => (
                    <div
                      key={idx}
                      className="group relative mt-2 px-3 py-2 text-sm text-gray-100 hover:bg-gray-800 rounded-md transition-colors"
                    >
                      <button
                        onClick={() => handleLoadChat(idx)}
                        className="w-full text-left truncate pr-8"
                      >
                        {c.title || `Chat ${idx + 1}`}
                      </button>
                      <button
                        onClick={(e) => handleDeleteChat(idx, e)}
                        className="absolute right-2 top-1/2 transform -translate-y-1/2 p-1 opacity-0 group-hover:opacity-100 hover:bg-gray-700 rounded transition-all duration-200"
                        title="Delete chat"
                      >
                        <Trash2 className="w-4 h-4 text-gray-400 hover:text-red-400" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </aside>
        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <div 
            ref={chatAreaRef} 
            className={`flex-1 p-4 px-6 flex flex-col overflow-y-auto scrollbar-hide`}
          >
            {messages.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center text-gray-200">
                <Bot className="w-16 h-16 text-blue-500 mb-6" />
                <p className="text-center text-lg">Ask me about major and skills that you want to prepare for the major</p>
              </div>
            ) : (
              <div className="max-w-[900px] mx-auto w-full space-y-4 pb-4">
                {messages.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg break-words whitespace-pre-wrap ${
                      msg.role === 'user' ? 'bg-gray-800 text-white' : 'bg-gray-800 text-white'
                    }`}>
                      {msg.content}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Chat input - anchored to bottom */}
          <div 
            ref={inputContainerRef}
            className="flex-shrink-0 p-4 pb-6 bg-gradient-to-t from-black via-black/80 to-transparent"
          >
            <div className="mx-auto max-w-full md:max-w-[900px]">
              <div className="w-full bg-[#111111]/90 backdrop-blur-md rounded-2xl p-3 py-[2px] shadow-lg border border-[#1f1f1f] focus-within:ring-1 focus-within:ring-blue-500 transition-all duration-200">
                <textarea
                  ref={textareaRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                  placeholder="Ask agent a question..."
                  className="w-full bg-[#111111] placeholder-gray-500 text-gray-200 px-4 py-3 rounded-lg focus:outline-none text-sm min-h-[60px] max-h-[200px] resize-none overflow-y-auto custom-scrollbar"
                />
                <div className="mt-3 flex items-center justify-between">
                  <button className="p-2 text-gray-300 hover:text-white">
                    <Paperclip className="w-5 h-5" />
                  </button>
                  <button onClick={handleSend} className="p-3 mx-2 my-2 bg-white/6 hover:bg-white/10 rounded-md">
                    <ArrowUp className="w-5 h-5 text-white" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}