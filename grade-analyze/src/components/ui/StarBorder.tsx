import React from 'react';

interface StarBorderProps {
  className?: string;
  color?: string;
  speed?: string;
  thickness?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}

const StarBorder: React.FC<StarBorderProps> = ({
  className = '',
  color = '#3b82f6',
  speed = '6s',
  thickness = 2,
  children,
  style,
}) => {
  return (
    <div
      className={`relative inline-block rounded-2xl ${className}`}
      style={{
        padding: `${thickness}px`,
        overflow: 'hidden',
        ...style
      }}
    >
      {/* Single glow element that travels around the border */}
      <div
        className="absolute opacity-70 rounded-full animate-star-border-loop z-0"
        style={{
          background: `radial-gradient(ellipse 200px 80px at center, ${color}, transparent 40%)`,
          animationDuration: speed,
          width: '200px',
          height: '80px',
        }}
      />
      <div className="relative z-10 bg-[#111111] border border-[#1f1f1f] rounded-2xl" style={{ borderRadius: 'calc(1rem - 2px)' }}>
        {children}
      </div>
    </div>
  );
};

export default StarBorder;

