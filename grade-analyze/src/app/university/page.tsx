"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
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
} from "lucide-react";
import Input from "@/components/ui/Input";
import Image from "next/image";

export default function UniversityPage() {
  const router = useRouter();
  const [universities, setUniversities] = useState<University[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterLocation, setFilterLocation] = useState("all");
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [hasToken, setHasToken] = useState<boolean | null>(null);
  const [user, setUser] = useState<{ name: string; email?: string } | null>(
    null
  );
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef<HTMLDivElement>(null);

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
    window.location.href = "/landing";
  };

  const filteredUniversities = universities.filter((uni) => {
    const matchesSearch =
      uni.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      uni.programs.some((p) =>
        p.toLowerCase().includes(searchQuery.toLowerCase())
      ) ||
      uni.location.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesLocation =
      filterLocation === "all" || uni.location === filterLocation;

    return matchesSearch && matchesLocation;
  });

  const uniqueLocations = Array.from(
    new Set(universities.map((u) => u.location))
  ).sort();

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
          filter: "brightness(0.3)",
          zIndex: 0,
          pointerEvents: "none",
        }}
      />

      {/* Header */}
      <header
        className="bg-white/2 backdrop-blur-md"
        style={{
          padding: "16px 0",
          position: "sticky",
          top: 0,
          zIndex: 100,
        }}
      >
        <div
          style={{ maxWidth: "1200px", margin: "0 auto", padding: "0 24px" }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              position: "relative",
            }}
          >
            {/* Logo */}
            <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <button
                onClick={() => router.push("/Input")}
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

            {/* Navigation Links - Centered */}
            <div
              className="flex items-center space-x-8"
              style={{
                position: "absolute",
                left: "50%",
                transform: "translateX(-50%)",
              }}
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
                gap: "16px",
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
                  <span className="hidden sm:inline">
                    {user?.name || "User"}
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

      <div className="relative z-10">
        {/* Search and Filter */}
        <div className="container mx-auto px-6 py-4">
          <div className="mb-8 flex flex-col md:flex-row gap-4 items-center justify-center">
            <div className="relative w-full md:w-[600px]">
              <Image
                src="/logo.svg"
                alt="Logo"
                width={24}
                height={24}
                className="absolute left-4 top-1/2 transform -translate-y-1/2"
              />
              <input
                type="text"
                placeholder="Search universities, programs, or locations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-12 pr-12 py-3 w-full bg-gray-800 border border-gray-700 text-white placeholder-gray-500 rounded-full focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
              />
              <button
                onClick={() => {
                  // Trigger search or filter action
                }}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1.5 hover:bg-gray-700 rounded-full transition-colors"
              >
                <Search className="w-5 h-5 text-gray-400 hover:text-white" />
              </button>
            </div>
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 pointer-events-none" />
              <select
                value={filterLocation}
                onChange={(e) => setFilterLocation(e.target.value)}
                className="pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none"
              >
                <option value="all">All Locations</option>
                {uniqueLocations.map((location) => (
                  <option key={location} value={location}>
                    {location}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Universities Grid */}
          {loading ? (
            <div className="text-center py-20">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
              <p className="mt-4 text-gray-400">Loading universities...</p>
            </div>
          ) : filteredUniversities.length === 0 ? (
            <div className="text-center py-20">
              <GraduationCap className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <p className="text-xl text-gray-400 mb-2">
                No universities found
              </p>
              <p className="text-gray-500">
                Try adjusting your search or filter criteria
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {filteredUniversities.map((university) => (
                <UniversityCard key={university.name} university={university} />
              ))}
            </div>
          )}

          {/* Results count */}
          {!loading && (
            <div className="text-center text-gray-400 mb-4">
              Showing {filteredUniversities.length} of {universities.length}{" "}
              universities
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
