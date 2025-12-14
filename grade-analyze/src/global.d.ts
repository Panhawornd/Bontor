import * as THREE from 'three';
import * as ReactThreeFiber from '@react-three/fiber';

export { };

declare module '*.glb' {
  const value: string;
  export default value;
}

declare module '*.png' {
  const value: string;
  export default value;
}

declare module '*.json' {
  const value: Record<string, unknown>;
  export default value;
}

declare module 'meshline' {
  export const MeshLineGeometry: new () => THREE.BufferGeometry;
  export const MeshLineMaterial: new (props?: Record<string, unknown>) => THREE.Material;
}

declare global {
  namespace JSX {
    interface IntrinsicElements {
      meshLineGeometry: ReactThreeFiber.Node<THREE.BufferGeometry, typeof import('meshline').MeshLineGeometry>;
      meshLineMaterial: ReactThreeFiber.MaterialNode<THREE.Material, typeof import('meshline').MeshLineMaterial>;
    }
  }
}

