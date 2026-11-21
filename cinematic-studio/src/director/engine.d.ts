declare module '*/engine/analyze.js' { export function analyze(description: string, opts?: { videoType?: string; style?: string }): any; }
declare module '*/engine/storyboard.js' {
  export function buildStoryboard(t: any, o: { duration: number; clip: { min: number; max: number }; lang: string }): any[];
  export function alternateScene(scene: any, t: any, lang: string, neighbours?: string[]): any;
  export function describeScene(role: string, t: any, lang: string, variant?: number): string;
}
declare module '*/engine/catalog.js' {
  type Item = { id: string; ar: string; en: string; p?: string; [k: string]: any };
  export const cameraMoves: Item[]; export const shotSizes: Item[]; export const videoTypes: Item[]; export const styles: Item[];
  export function byId(list: Item[], id: string): Item | undefined;
}
