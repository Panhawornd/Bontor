"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Button from "@/components/ui/Button";
import UniversityCard, { University } from "@/components/UniversityCard";
import {
  GraduationCap,
  ArrowLeft,
  Search,
  Filter,
  User,
  LogOut,
  ChevronDown,
  ArrowRight,
  BookOpen,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import Input from "@/components/ui/Input";
import Image from "next/image";

export default function UniversityPage() {
  const router = useRouter();
  const [universities, setUniversities] = useState<University[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState<"all" | "recommended">("all");
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [hasToken, setHasToken] = useState<boolean | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 9;
  const [user, setUser] = useState<{ name: string; email?: string } | null>(
    null
  );
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);

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
      }
    };

    checkAuth();

    const fetchUniversities = async () => {
      try {
        const response = await fetch("/api/universities");
        if (!response.ok) {
          throw new Error("Failed to fetch universities");
        }
        const data = await response.json();
        setUniversities(data.universities);
      } catch (error) {
        console.error("Error fetching universities:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUniversities();
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

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    localStorage.setItem('just_logged_out', 'true');
    localStorage.removeItem('just_logged_in');
    window.location.href = "/landing";
  };

  const filteredUniversities = universities.filter((uni) => {
    const matchesSearch =
      uni.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (uni.availablePrograms || []).some((p: string) =>
        p.toLowerCase().includes(searchQuery.toLowerCase())
      ) ||
      (uni.city || "").toLowerCase().includes(searchQuery.toLowerCase());

    return matchesSearch;
  });

  // Pagination logic
  const totalPages = Math.ceil(filteredUniversities.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const paginatedUniversities = filteredUniversities.slice(startIndex, endIndex);

  // Reset to page 1 when search changes
  useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery]);

  // Scroll to top when page changes
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [currentPage]);

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
        {/* Ultravib image background with dark overlay */}
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
    <div className="min-h-screen text-white relative">
      {/* Ultravib image background with dark overlay */}
      <div
        className="fixed inset-x-0"
        style={{
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
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
        className="bg-white/2 backdrop-blur-md"
        style={{
          padding: "16px 0",
          minHeight: "4rem",
          position: "sticky",
          top: 0,
          zIndex: 100,
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
              <Link
                href="/landing"
                className="hover:opacity-80 transition-opacity"
                style={{ padding: 0 }}
              >
                <img
                  src="/image/Bontor-logo.png"
                  alt="Bontor"
                  className="h-5 md:h-[23px] w-auto"
                />
              </Link>
            </div>

            {/* Navigation Links - Centered - Hidden on mobile */}
            <div
              className="hidden lg:flex items-center space-x-8"
              style={{ position: "absolute", left: "50%", transform: "translateX(-50%)" }}
            >
              <Link
                href="/Input"
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Analyze
              </Link>
              <Link
                href="/dashboard"
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/university"
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                University
              </Link>
              <Link
                href="/agent"
                className="px-3 py-2 rounded-md text-sm font-medium text-white hover:text-white hover:bg-gray-800 transition-colors"
              >
                Agent
              </Link>
            </div>

            {/* Profile Menu */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "8px",
                position: "relative",
                justifySelf: 'end'
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
              <Link href="/Input" onClick={() => setIsMenuOpen(false)} className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors">
                Analyze
              </Link>
              <Link href="/dashboard" onClick={() => setIsMenuOpen(false)} className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors">
                Dashboard
              </Link>
              <Link href="/university" onClick={() => setIsMenuOpen(false)} className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors">
                University
              </Link>
              <Link href="/agent" onClick={() => setIsMenuOpen(false)} className="text-left uppercase tracking-wide text-white/90 hover:text-white transition-colors">
                Agent
              </Link>
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

      <div className="relative z-10 pt-10">
        {/* Search and Toggle */}
        <div className="container mx-auto px-6 py-4">
          <div className="mb-8 flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="relative w-full md:w-[400px]">
              <Image
                src="/logo.svg"
                alt="Logo"
                width={24}
                height={24}
                className="absolute left-4 top-1/2 transform -translate-y-1/2"
              />
              <input
                ref={searchInputRef}
                type="text"
                placeholder="Search universities..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-12 pr-12 py-3 w-full bg-gray-800 border border-gray-700 text-white placeholder-gray-500 rounded-full focus:outline-none focus:border-blue-500 transition-all"
                style={{
                  boxShadow: 'none'
                }}
                onFocus={(e) => {
                  e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.boxShadow = 'none';
                }}
              />
              <button
                onClick={() => {
                  searchInputRef.current?.focus();
                }}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1.5 hover:bg-gray-700 rounded-full transition-colors"
              >
                <Search className="w-5 h-5 text-gray-400 hover:text-white" />   
              </button>
            </div>

            {/* Toggle Filter */}
            <div style={{ 
              display: 'flex', 
              gap: '12px',
              backgroundColor: '#1a1a1a',
              padding: '4px',
              borderRadius: '8px',
              border: '1px solid #2a2a2a'
            }}>
              <button
                type="button"
                onClick={() => setFilterType("all")}
                style={{
                  padding: '10px 24px',
                  borderRadius: '6px',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  backgroundColor: filterType === "all" ? '#1f2937' : 'transparent',
                  color: filterType === "all" ? '#ffffff' : '#9ca3af',
                  border: 'none',
                  outline: 'none'
                }}
              >
                All
              </button>
              <button
                type="button"
                onClick={() => setFilterType("recommended")}
                style={{
                  padding: '10px 24px',
                  borderRadius: '6px',
                  fontSize: '14px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  backgroundColor: filterType === "recommended" ? '#1f2937' : 'transparent',
                  color: filterType === "recommended" ? '#ffffff' : '#9ca3af',
                  border: 'none',
                  outline: 'none'
                }}
              >
                Recommended
              </button>
            </div>
          </div>

          {/* Universities Grid */}
          {filterType === "recommended" ? (
            <div className="text-center py-20">
              <BookOpen className="w-16 h-16 text-blue-500 mx-auto mb-6" />
              <p className="text-lg text-gray-200 mb-6 max-w-2xl mx-auto">
                Complete your academic analysis on the Analyze page to receive university recommendations.
              </p>
              <Link
                href="/Input"
                className="group inline-flex items-center gap-3 px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-md transition-colors border border-gray-600"
              >
                Go to Analyze
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </div>
          ) : loading ? (
            <div className="text-center py-20">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
              <p className="mt-4 text-gray-400">Loading universities...</p>
            </div>
          ) : filteredUniversities.length === 0 ? (
            <div className="text-center py-20">
              <GraduationCap className="w-16 h-16 text-blue-500 mx-auto mb-6" />
              <p className="text-lg text-gray-200 mb-6 max-w-2xl mx-auto">
                No universities found. Try adjusting your search criteria.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {paginatedUniversities.map((university) => (
                <UniversityCard key={university.name} university={university} />
              ))}
            </div>
          )}

          {/* Pagination Controls */}
          {!loading && filterType !== "recommended" && filteredUniversities.length > 0 && (
            <div className="flex flex-col items-center gap-4 mb-8">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                  disabled={currentPage === 1}
                  className="p-2 bg-gray-800 hover:bg-gray-700 disabled:bg-gray-900 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-md transition-colors border border-gray-600"
                  aria-label="Previous page"
                >
                  <ChevronLeft className="w-5 h-5" />
                </button>
                
                <div className="flex items-center gap-1">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                    <button
                      key={page}
                      onClick={() => setCurrentPage(page)}
                      className={`w-10 h-10 rounded-md transition-colors ${
                        currentPage === page
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-800 hover:bg-gray-700 text-white border border-gray-600'
                      }`}
                    >
                      {page}
                    </button>
                  ))}
                </div>

                <button
                  onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                  disabled={currentPage === totalPages}
                  className="p-2 bg-gray-800 hover:bg-gray-700 disabled:bg-gray-900 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-md transition-colors border border-gray-600"
                  aria-label="Next page"
                >
                  <ChevronRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
