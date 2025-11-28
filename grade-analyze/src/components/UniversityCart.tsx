"use client";

import Image from "next/image";
import { useState, useEffect } from "react";
import { ShoppingCart, X, Trash2 } from "lucide-react";
import Button from "./ui/Button";
import { University } from "./UniversityCard";

interface UniversityCartProps {
  cart: University[];
  onRemoveFromCart: (universityName: string) => void;
  onClearCart: () => void;
  isOpen: boolean;
  onToggle: () => void;
}

export default function UniversityCart({
  cart,
  onRemoveFromCart,
  onClearCart,
  isOpen,
  onToggle,
}: UniversityCartProps) {
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setIsAnimating(true);
      const timer = setTimeout(() => setIsAnimating(false), 300);
      return () => clearTimeout(timer);
    }
  }, [isOpen]);

  return (
    <>
      <button
        onClick={onToggle}
        className="fixed bottom-6 right-6 bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-lg transition-all duration-300 hover:scale-110 z-50 flex items-center gap-2"
      >
        <ShoppingCart className="w-6 h-6" />
        {cart.length > 0 && (
          <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center">
            {cart.length}
          </span>
        )}
      </button>

      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300"
          onClick={onToggle}
        />
      )}

      <div
        className={`fixed top-0 right-0 h-full w-full md:w-96 bg-gray-900 border-l border-gray-700 shadow-2xl z-50 transform transition-transform duration-300 ease-in-out ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-between p-6 border-b border-gray-700">
            <div className="flex items-center gap-3">
              <ShoppingCart className="w-6 h-6 text-blue-500" />
              <h2 className="text-xl font-bold text-white">
                University Cart ({cart.length})
              </h2>
            </div>
            <button
              onClick={onToggle}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4">
            {cart.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <ShoppingCart className="w-16 h-16 text-gray-600 mb-4" />
                <p className="text-gray-400 text-lg mb-2">Your cart is empty</p>
                <p className="text-gray-500 text-sm">
                  Add universities to compare them
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {cart.map((university, index) => {
                  const thumbnail =
                    university.imageUrl ?? "/image/Bontor-logo.png";

                  return (
                    <div
                      key={index}
                      className="bg-gray-800 border border-gray-700 rounded-lg p-4 transition-all hover:border-blue-500"
                    >
                      <div className="flex gap-3 mb-3">
                        <div className="relative w-16 h-16 rounded-md overflow-hidden border border-gray-700 flex-shrink-0 bg-gray-900">
                          <Image
                            src={thumbnail}
                            alt={`Bontor logo for ${university.name}`}
                            fill
                            sizes="64px"
                            className="object-contain p-1"
                          />
                        </div>
                        <div className="flex-1">
                          <div className="flex justify-between items-start">
                            <h3 className="text-white font-semibold text-sm flex-1">
                              {university.name}
                            </h3>
                            <button
                              onClick={() => onRemoveFromCart(university.name)}
                              className="text-gray-400 hover:text-red-500 transition-colors ml-2"
                            >
                              <X className="w-5 h-5" />
                            </button>
                          </div>
                          <p className="text-gray-400 text-xs mb-1">
                            {university.location}, {university.country}
                          </p>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {u                              .map((progr, pIndex) => (
                          <span
                            key={pIndex}
                              className="text-xs bg-gray-700 text-gray-300 px py-1 rounded"
                          >
                            {program}
                          </span>
                          ))}
                        {university.programs.length > 3 && (
                          <span className="text-xs text-gray-500 px-2 py-1">
                            +{university.programs.length - 3}
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {cart.length > 0 && (
            <div className="border-t border-gray-700 p-4">
              <Button
                onClick={onClearCart}
                className="w-full bg-red-600 hover:bg-red-700 text-white py-3 rounded-lg flex items-center justify-center gap-2 transition-colors"
              >
                <Trash2 className="w-5 h-5" />
                Clear Cart
              </Button>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
