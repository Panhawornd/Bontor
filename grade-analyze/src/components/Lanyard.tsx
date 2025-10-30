/* eslint-disable react/no-unknown-property */
'use client';
import { useEffect, useRef, useState, useMemo } from 'react';
import { Canvas, extend, useFrame } from '@react-three/fiber';
import { useGLTF, useTexture, Environment, Lightformer } from '@react-three/drei';
import { BallCollider, CuboidCollider, Physics, RigidBody, useRopeJoint, useSphericalJoint } from '@react-three/rapier';
import { MeshLineGeometry, MeshLineMaterial } from 'meshline';
import * as THREE from 'three';

// Note: You need to add card.glb and lanyard.png to public/assets/lanyard/
// For now, using placeholder - replace with actual imports when assets are available
// import cardGLB from '/assets/lanyard/card.glb';
// import lanyard from '/assets/lanyard/lanyard.png';

extend({ MeshLineGeometry, MeshLineMaterial });

interface LanyardProps {
  position?: [number, number, number];
  gravity?: [number, number, number];
  fov?: number;
  transparent?: boolean;
  scale?: number;
}

function SimpleCard() {
  const [hovered, setHovered] = useState(false);
  const groupRef = useRef<THREE.Group>(null);

  // Create rounded rectangle shape with corner radius
  const cardShape = useMemo(() => {
    const shape = new THREE.Shape();
    const width = 4;
    const height = 6;
    const radius = 0.3;
    
    shape.moveTo(-width / 2 + radius, -height / 2);
    shape.lineTo(width / 2 - radius, -height / 2);
    shape.quadraticCurveTo(width / 2, -height / 2, width / 2, -height / 2 + radius);
    shape.lineTo(width / 2, height / 2 - radius);
    shape.quadraticCurveTo(width / 2, height / 2, width / 2 - radius, height / 2);
    shape.lineTo(-width / 2 + radius, height / 2);
    shape.quadraticCurveTo(-width / 2, height / 2, -width / 2, height / 2 - radius);
    shape.lineTo(-width / 2, -height / 2 + radius);
    shape.quadraticCurveTo(-width / 2, -height / 2, -width / 2 + radius, -height / 2);
    
    return shape;
  }, []);

  useFrame((state) => {
    if (groupRef.current) {
      const targetRotation = hovered ? 0.1 : 0;
      const targetScale = hovered ? 1.05 : 1;
      
      groupRef.current.rotation.y += (targetRotation - groupRef.current.rotation.y) * 0.1;
      groupRef.current.scale.x += (targetScale - groupRef.current.scale.x) * 0.1;
      groupRef.current.scale.y += (targetScale - groupRef.current.scale.y) * 0.1;
      groupRef.current.scale.z += (targetScale - groupRef.current.scale.z) * 0.1;
    }
  });

  return (
    <group 
      ref={groupRef}
      onPointerEnter={() => setHovered(true)}
      onPointerLeave={() => setHovered(false)}
    >
      {/* White ID Card with rounded corners */}
      <mesh position={[0, 0, 0]}>
        <extrudeGeometry args={[cardShape, { depth: 0.05, bevelEnabled: false }]} />
        <meshStandardMaterial color="#ffffff" />
      </mesh>
      {/* Hole at top of card for lanyard hook - dark hole effect */}
      <mesh position={[0, 2.6, 0.025]}>
        <cylinderGeometry args={[0.25, 0.25, 0.15, 16]} />
        <meshStandardMaterial color="#000000" />
      </mesh>
      {/* Orange lanyard strap at top */}
      <mesh position={[0, 3.2, 0]}>
        <boxGeometry args={[0.4, 0.8, 0.03]} />
        <meshStandardMaterial color="#ffffff" />
      </mesh>
      {/* Orange lanyard band extending up */}
      <mesh position={[0, 4.4, 0]}>
        <boxGeometry args={[0.3, 2.5, 0.02]} />
        <meshStandardMaterial color="#f97316" />
      </mesh>
      {/* Orange neckwear loop at the top */}
      <mesh position={[0, 6.2, 0]}>
        <torusGeometry args={[0.4, 0.15, 8, 16]} />
        <meshStandardMaterial color="#f97316" />
      </mesh>
      {/* Orange neckwear strap behind the loop */}
      <mesh position={[0, 6.2, -0.2]}>
        <boxGeometry args={[1, 0.3, 0.05]} />
        <meshStandardMaterial color="#f97316" />
      </mesh>
    </group>
  );
}

export default function Lanyard({ 
  position = [0, 0, 11], 
  gravity = [0, -40, 0], 
  fov = 42, 
  transparent = true,
  scale = 1 
}: LanyardProps) {
  return (
    <div className="relative z-0 w-full h-full" style={{ width: '100%', height: '100%' }}>
      <Canvas
        camera={{ position: position, fov: fov }}
        gl={{ alpha: transparent }}
        onCreated={({ gl }) => {
          gl.setClearColor(new THREE.Color(0x000000), transparent ? 0 : 1);
        }}
        style={{ width: '100%', height: '100%', display: 'block' }}
      >
        <ambientLight intensity={2} />
        <directionalLight position={[2, 2, 5]} intensity={1.5} />
        <SimpleCard />
      </Canvas>
    </div>
  );
}

function Band({ maxSpeed = 50, minSpeed = 0 }: { maxSpeed?: number; minSpeed?: number }) {
  const band = useRef<THREE.Mesh>(null),
    fixed = useRef<any>(null),
    j1 = useRef<any>(null),
    j2 = useRef<any>(null),
    j3 = useRef<any>(null),
    card = useRef<any>(null);
  const vec = new THREE.Vector3(),
    ang = new THREE.Vector3(),
    rot = new THREE.Vector3(),
    dir = new THREE.Vector3();
  const segmentProps: any = { type: 'dynamic', canSleep: true, colliders: false, angularDamping: 4, linearDamping: 4 };
  
  // Placeholder - replace with actual GLB when available
  // const { nodes, materials } = useGLTF(cardGLB);
  // const texture = useTexture(lanyard);
  
  const [curve] = useState(
    () =>
      new THREE.CatmullRomCurve3([new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3()])
  );
  const [dragged, drag] = useState<THREE.Vector3 | false>(false);
  const [hovered, hover] = useState(false);
  const [isSmall, setIsSmall] = useState(() => typeof window !== 'undefined' && window.innerWidth < 1024);

  useRopeJoint(fixed, j1, [[0, 0, 0], [0, 0, 0], 1]);
  useRopeJoint(j1, j2, [[0, 0, 0], [0, 0, 0], 1]);
  useRopeJoint(j2, j3, [[0, 0, 0], [0, 0, 0], 1]);
  useSphericalJoint(j3, card, [
    [0, 0, 0],
    [0, 1.5, 0]
  ]);

  useEffect(() => {
    if (hovered) {
      document.body.style.cursor = dragged ? 'grabbing' : 'grab';
      return () => void (document.body.style.cursor = 'auto');
    }
  }, [hovered, dragged]);

  useEffect(() => {
    const handleResize = () => {
      setIsSmall(window.innerWidth < 1024);
    };

    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useFrame((state, delta) => {
    if (dragged && card.current) {
      vec.set(state.pointer.x, state.pointer.y, 0.5).unproject(state.camera);
      dir.copy(vec).sub(state.camera.position).normalize();
      vec.add(dir.multiplyScalar(state.camera.position.length()));
      [card, j1, j2, j3, fixed].forEach(ref => ref.current?.wakeUp?.());
      if (card.current && dragged instanceof THREE.Vector3) {
        card.current.setNextKinematicTranslation?.({ x: vec.x - dragged.x, y: vec.y - dragged.y, z: vec.z - dragged.z });
      }
    }
    if (fixed.current) {
      [j1, j2].forEach(ref => {
        if (ref.current && !(ref.current as any).lerped) {
          (ref.current as any).lerped = new THREE.Vector3().copy(ref.current.translation());
        }
        if (ref.current && (ref.current as any).lerped) {
          const clampedDistance = Math.max(0.1, Math.min(1, (ref.current as any).lerped.distanceTo(ref.current.translation())));
          (ref.current as any).lerped.lerp(
            ref.current.translation(),
            delta * (minSpeed + clampedDistance * (maxSpeed - minSpeed))
          );
        }
      });
      if (j3.current && card.current && band.current) {
        curve.points[0].copy(j3.current.translation());
        curve.points[1].copy((j2.current as any)?.lerped || new THREE.Vector3());
        curve.points[2].copy((j1.current as any)?.lerped || new THREE.Vector3());
        curve.points[3].copy(fixed.current.translation());
        (band.current as any).geometry.setPoints(curve.getPoints(32));
        if (card.current.angvel) {
          ang.copy(card.current.angvel());
          rot.copy(card.current.rotation());
          card.current.setAngvel({ x: ang.x, y: ang.y - rot.y * 0.25, z: ang.z });
        }
      }
    }
  });

  curve.curveType = 'chordal';
  
  // Placeholder rendering until assets are available
  return (
    <>
      <group position={[0, 4, 0]}>
        <RigidBody ref={fixed} {...segmentProps} type="fixed" />
        <RigidBody position={[0.5, 0, 0]} ref={j1} {...segmentProps}>
          <BallCollider args={[0.1]} />
        </RigidBody>
        <RigidBody position={[1, 0, 0]} ref={j2} {...segmentProps}>
          <BallCollider args={[0.1]} />
        </RigidBody>
        <RigidBody position={[1.5, 0, 0]} ref={j3} {...segmentProps}>
          <BallCollider args={[0.1]} />
        </RigidBody>
        <RigidBody position={[2, 0, 0]} ref={card} {...segmentProps} type={dragged ? 'kinematicPosition' : 'dynamic'}>
          <CuboidCollider args={[0.8, 1.125, 0.01]} />
          <group
            scale={1.5}
            position={[0, -1.2, -0.05]}
            onPointerOver={() => hover(true)}
            onPointerOut={() => hover(false)}
            onPointerUp={(e: any) => {
              e.target.releasePointerCapture(e.pointerId);
              drag(false);
            }}
            onPointerDown={(e: any) => {
              e.target.setPointerCapture(e.pointerId);
              const cardPos = card.current?.translation?.() || new THREE.Vector3();
              drag(new THREE.Vector3().copy(e.point).sub(vec.copy(cardPos)));
            }}
          >
            {/* Placeholder card - replace with GLB when available */}
            <mesh>
              <boxGeometry args={[1.8, 2.5, 0.05]} />
              <meshStandardMaterial
                color="#2a2a2a"
                metalness={0.5}
                roughness={0.3}
              />
            </mesh>
            <mesh position={[0, 0, 0.026]}>
              <boxGeometry args={[1.75, 2.45, 0.001]} />
              <meshStandardMaterial color="#ffffff" />
            </mesh>
          </group>
        </RigidBody>
      </group>
      <mesh ref={band}>
        {/* @ts-ignore */}
        <meshLineGeometry />
        {/* @ts-ignore */}
        <meshLineMaterial
          color="white"
          depthTest={false}
          resolution={isSmall ? [1000, 2000] : [1000, 1000]}
          useMap={false}
          lineWidth={1}
        />
      </mesh>
    </>
  );
}

