/** Vocabulary shared by the engine, the API and the UI (labels are bilingual; `p` is the prompt phrase). */
export const cameraMoves = [
  { id: 'static', ar: 'ثابتة على حامل', en: 'Static (locked off)', p: 'locked-off tripod shot with subtle natural movement in frame' },
  { id: 'dolly_in', ar: 'Dolly In — اقتراب', en: 'Dolly In', p: 'slow, smooth dolly-in toward the subject' },
  { id: 'dolly_out', ar: 'Dolly Out — ابتعاد', en: 'Dolly Out', p: 'slow, smooth dolly-out revealing the surroundings' },
  { id: 'tracking', ar: 'Tracking Shot — تتبع', en: 'Tracking Shot', p: 'steady tracking shot moving alongside the subject at matching speed' },
  { id: 'crane_up', ar: 'Crane Up — رافعة صاعدة', en: 'Crane Up', p: 'crane shot rising smoothly to reveal the scene' },
  { id: 'crane_down', ar: 'Crane Down — رافعة هابطة', en: 'Crane Down', p: 'crane shot descending smoothly toward the subject' },
  { id: 'drone', ar: 'Drone Shot — جوية', en: 'Drone Shot', p: 'smooth aerial drone shot gliding forward' },
  { id: 'pan', ar: 'Pan — مسح أفقي', en: 'Pan', p: 'slow horizontal pan across the scene' },
  { id: 'tilt', ar: 'Tilt — إمالة عمودية', en: 'Tilt', p: 'slow vertical tilt revealing the subject' },
  { id: 'orbit', ar: 'Orbit — دوران حول العنصر', en: 'Orbit', p: 'slow orbiting camera arc around the subject' },
  { id: 'handheld', ar: 'Handheld Cinematic — محمولة', en: 'Handheld Cinematic', p: 'handheld cinematic camera with gentle organic sway' },
];
export const shotSizes = [
  { id: 'wide', ar: 'واسعة', en: 'Wide', p: 'Wide establishing shot' },
  { id: 'medium_wide', ar: 'متوسطة واسعة', en: 'Medium wide', p: 'Medium-wide shot' },
  { id: 'medium', ar: 'متوسطة', en: 'Medium', p: 'Medium shot' },
  { id: 'close', ar: 'قريبة', en: 'Close-up', p: 'Close-up' },
  { id: 'macro', ar: 'قريبة جدًا (تفاصيل)', en: 'Extreme close-up', p: 'Extreme close-up macro detail shot' },
];
export const videoTypes = [
  { id: 'commercial', ar: 'إعلان تجاري', en: 'Commercial' },
  { id: 'short_film', ar: 'فيلم قصير', en: 'Short film' },
  { id: 'tourism', ar: 'فيديو سياحي', en: 'Tourism' },
  { id: 'real_estate', ar: 'عقاري وفندقي', en: 'Real estate & hospitality' },
  { id: 'product', ar: 'فيديو منتج', en: 'Product' },
  { id: 'creative', ar: 'سينمائي إبداعي', en: 'Creative cinematic' },
  { id: 'social', ar: 'منصات التواصل', en: 'Social media' },
  { id: 'motion_graphics', ar: 'موشن جرافيك', en: 'Motion graphics' },
];
export const styles = [
  { id: 'auto', ar: 'تلقائي (يحدده المخرج)', en: 'Auto (director decides)' },
  { id: 'realism', ar: 'واقعية سينمائية', en: 'Cinematic realism', lens: '35mm anamorphic lens', grade: 'natural filmic grade with rich contrast and true-to-life skin tones', look: 'anamorphic film look, subtle lens flares', grain: true, pace: 'measured' },
  { id: 'noir', ar: 'نيو-نوار', en: 'Neo-noir', lens: '40mm anamorphic lens', grade: 'teal-and-magenta neon noir grade, deep blacks, saturated practical lights', look: 'moody neo-noir film look with halation around highlights', grain: true, pace: 'measured', light: 'neon' },
  { id: 'epic', ar: 'ملحمي', en: 'Epic', lens: '24mm wide anamorphic lens', grade: 'bold high-contrast grade with warm highlights and cool shadows', look: 'large-format epic film look', grain: false, pace: 'slow' },
  { id: 'luxury', ar: 'إعلاني فاخر', en: 'Luxury commercial', lens: '85mm prime lens', grade: 'clean premium grade, soft highlight roll-off, rich blacks, restrained palette', look: 'polished high-end commercial look', grain: false, pace: 'slow' },
  { id: 'documentary', ar: 'وثائقي', en: 'Documentary', lens: '28mm spherical lens', grade: 'neutral naturalistic grade', look: 'observational documentary look', grain: true, pace: 'measured', light: 'natural' },
  { id: 'dreamy', ar: 'حالم', en: 'Dreamy', lens: '50mm vintage lens with soft bloom', grade: 'soft pastel grade with lifted shadows and gentle glow', look: 'dreamlike soft-focus look', grain: true, pace: 'slow' },
  { id: 'vintage', ar: 'فيلم كلاسيكي', en: 'Vintage film', lens: '35mm vintage spherical lens', grade: 'warm Kodak-style film emulation with faded blacks', look: '35mm celluloid look with gate weave', grain: true, pace: 'measured' },
  { id: 'minimal', ar: 'نظيف وبسيط', en: 'Clean minimal', lens: '50mm prime lens', grade: 'bright clean grade with neutral whites and soft contrast', look: 'minimal modern look with generous negative space', grain: false, pace: 'measured' },
  { id: 'energetic', ar: 'سريع وحماسي', en: 'High energy', lens: '18mm wide lens', grade: 'punchy saturated grade with crisp contrast', look: 'dynamic sports-commercial look', grain: false, pace: 'fast' },
];
export const byId = (list, id) => list.find((x) => x.id === id);
