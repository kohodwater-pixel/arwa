/**
 * Bilingual lexicon of the rule-based director. Each concept: [id, group, English production term,
 * Arabic label, Arabic stems, English stems]. Arabic stems are matched after normalisation
 * (tashkeel removed, alef/ya/ta-marbuta unified) and allow the usual attached prefixes.
 */
const raw = [
  // time of day
  ['night', 'time', 'night', 'ليلًا', ['ليل', 'مساء', 'منتصف الليل'], ['night', 'midnight', 'nighttime', 'evening']],
  ['golden_hour', 'time', 'golden hour', 'وقت الغروب الذهبي', ['غروب', 'الساعه الذهبيه', 'ذهبي', 'مغيب'], ['sunset', 'golden hour', 'dusk glow']],
  ['dawn', 'time', 'dawn', 'عند الفجر', ['فجر', 'شروق', 'الصباح الباكر'], ['dawn', 'sunrise', 'daybreak', 'early morning']],
  ['blue_hour', 'time', 'blue hour', 'الساعة الزرقاء', ['الساعه الزرقاء', 'الشفق', 'بعد الغروب'], ['blue hour', 'twilight', 'dusk']],
  ['day', 'time', 'daytime', 'نهارًا', ['نهار', 'ظهيره', 'وضح النهار', 'صباح'], ['daytime', 'daylight', 'midday', 'noon', 'morning', 'sunny day']],
  // weather / atmosphere
  ['rain', 'weather', 'rain, wet reflective surfaces', 'تحت المطر', ['مطر', 'ممطر', 'امطار', 'مبلل'], ['rain', 'rainy', 'raining', 'wet street', 'drizzle']],
  ['snow', 'weather', 'falling snow', 'تحت الثلج', ['ثلج', 'ثلوج', 'مثلج'], ['snow', 'snowy', 'snowfall', 'blizzard']],
  ['fog', 'weather', 'fog and atmospheric haze', 'وسط الضباب', ['ضباب', 'ضبابي'], ['fog', 'foggy', 'mist', 'misty', 'haze']],
  ['storm', 'weather', 'storm clouds', 'في أجواء عاصفة', ['عاصف', 'عاصفه', 'برق', 'رعد'], ['storm', 'stormy', 'lightning', 'thunder']],
  ['dust', 'weather', 'dust and sand particles in the air', 'وسط الغبار', ['غبار', 'رمال متطايره', 'عاصفه رمليه'], ['dust', 'sandstorm', 'dusty']],
  ['sun', 'weather', 'clear sunlight', 'تحت الشمس', ['مشمس', 'شمس', 'سماء صافيه'], ['sunny', 'sunlight', 'clear sky', 'sunshine']],
  // environment
  ['city', 'env', 'city streets', 'شوارع المدينة', ['مدينه', 'شوارع', 'شارع', 'وسط البلد', 'ناطحات', 'ابراج'], ['city', 'street', 'streets', 'downtown', 'urban', 'skyline', 'skyscraper', 'skyscrapers']],
  ['desert', 'env', 'desert dunes', 'الصحراء', ['صحراء', 'كثبان', 'رمال', 'باديه'], ['desert', 'dunes', 'sand dunes']],
  ['sea', 'env', 'seaside', 'البحر', ['بحر', 'شاطئ', 'ساحل', 'محيط', 'امواج', 'كورنيش'], ['sea', 'ocean', 'beach', 'coast', 'shore', 'waves', 'seaside']],
  ['mountain', 'env', 'mountains', 'الجبال', ['جبل', 'جبال', 'قمه', 'وادي', 'منحدر'], ['mountain', 'mountains', 'peak', 'valley', 'cliff', 'canyon']],
  ['forest', 'env', 'forest', 'الغابة', ['غابه', 'غابات', 'اشجار', 'حديقه', 'نخيل', 'واحه'], ['forest', 'woods', 'trees', 'jungle', 'garden', 'park', 'oasis', 'palm']],
  ['interior', 'env', 'interior space', 'مساحة داخلية', ['داخل', 'غرفه', 'صاله', 'مطبخ', 'مكتب', 'جناح', 'ردهه', 'لوبي', 'مجلس', 'مقهى', 'مطعم'], ['interior', 'indoor', 'indoors', 'room', 'lobby', 'kitchen', 'office', 'suite', 'living room', 'cafe', 'restaurant', 'bedroom']],
  ['studio', 'env', 'studio set with seamless backdrop', 'استوديو', ['استوديو', 'خلفيه سوداء', 'خلفيه بيضاء'], ['studio', 'seamless backdrop', 'black background', 'white background']],
  ['heritage', 'env', 'historic architecture', 'معالم تراثية', ['تراث', 'قلعه', 'حصن', 'سوق قديم', 'اثار', 'قصر', 'مسجد', 'تاريخي'], ['heritage', 'historic', 'castle', 'fort', 'ruins', 'old town', 'palace', 'mosque', 'ancient']],
  ['space', 'env', 'outer space', 'الفضاء', ['فضاء', 'كوكب', 'مجره', 'نجوم'], ['space', 'planet', 'galaxy', 'stars', 'nebula', 'cosmos']],
  ['road', 'env', 'open road', 'الطريق', ['طريق', 'طريق سريع', 'جسر'], ['road', 'highway', 'bridge', 'freeway']],
  // subjects
  ['car', 'subject', 'car', 'السيارة', ['سياره', 'سيارات', 'مركبه'], ['car', 'cars', 'vehicle', 'supercar', 'suv', 'sedan']],
  ['sports_car', 'subject', 'sports car', 'السيارة الرياضية', ['سياره رياضيه', 'سياره سباق'], ['sports car', 'supercar', 'race car', 'hypercar']],
  ['motorcycle', 'subject', 'motorcycle', 'الدراجة النارية', ['دراجه ناريه'], ['motorcycle', 'motorbike']],
  ['man', 'subject', 'a man', 'الرجل', ['رجل', 'شاب', 'فارس', 'بطل'], ['man', 'guy', 'young man', 'businessman', 'hero']],
  ['woman', 'subject', 'a woman', 'المرأة', ['امراه', 'سيده', 'فتاه', 'شابه'], ['woman', 'girl', 'lady', 'young woman', 'businesswoman']],
  ['child', 'subject', 'a child', 'الطفل', ['طفل', 'طفله', 'اطفال'], ['child', 'kid', 'kids', 'children', 'boy']],
  ['family', 'subject', 'a family', 'العائلة', ['عائله', 'اسره'], ['family', 'couple']],
  ['people', 'subject', 'people', 'الناس', ['ناس', 'حشد', 'جمهور', 'زوار', 'سياح', 'ضيوف'], ['people', 'crowd', 'visitors', 'tourists', 'guests', 'audience']],
  ['product', 'subject', 'the product', 'المنتج', ['منتج', 'عبوه', 'علبه', 'زجاجه', 'قاروره'], ['product', 'bottle', 'package', 'packaging', 'box', 'can']],
  ['perfume', 'subject', 'perfume bottle', 'زجاجة العطر', ['عطر', 'عطور'], ['perfume', 'fragrance', 'cologne']],
  ['watch', 'subject', 'wristwatch', 'الساعة', ['ساعه يد', 'ساعه فاخره'], ['watch', 'wristwatch', 'timepiece']],
  ['phone', 'subject', 'smartphone', 'الهاتف', ['هاتف', 'جوال', 'موبايل'], ['phone', 'smartphone', 'mobile']],
  ['jewelry', 'subject', 'jewellery', 'المجوهرات', ['مجوهرات', 'خاتم', 'ذهب', 'الماس', 'عقد'], ['jewelry', 'jewellery', 'ring', 'necklace', 'diamond']],
  ['food', 'subject', 'the dish', 'الطبق', ['طعام', 'طبق', 'وجبه', 'برجر', 'بيتزا', 'حلوى', 'كيك', 'ماكولات', 'شوكولاته'], ['food', 'dish', 'meal', 'burger', 'pizza', 'dessert', 'cake', 'chocolate', 'steak']],
  ['coffee', 'subject', 'coffee', 'القهوة', ['قهوه', 'فنجان', 'اسبريسو', 'لاتيه'], ['coffee', 'espresso', 'latte', 'cappuccino']],
  ['building', 'subject', 'the building', 'المبنى', ['برج', 'مبنى', 'عماره', 'ناطحه سحاب', 'مجمع'], ['building', 'tower', 'skyscraper', 'complex']],
  ['villa', 'subject', 'luxury villa', 'الفيلا', ['فيلا', 'فلل', 'منزل', 'بيت', 'شقه', 'عقار'], ['villa', 'house', 'home', 'apartment', 'property', 'mansion', 'penthouse']],
  ['hotel', 'subject', 'hotel', 'الفندق', ['فندق', 'منتجع', 'فنادق'], ['hotel', 'resort']],
  ['pool', 'subject', 'swimming pool', 'المسبح', ['مسبح', 'حوض سباحه'], ['pool', 'swimming pool', 'infinity pool']],
  ['horse', 'subject', 'horse', 'الحصان', ['حصان', 'خيل', 'خيول', 'فرس'], ['horse', 'horses', 'stallion']],
  ['camel', 'subject', 'camel', 'الجمل', ['جمل', 'جمال', 'ابل', 'قافله'], ['camel', 'camels', 'caravan']],
  ['falcon', 'subject', 'falcon', 'الصقر', ['صقر', 'صقور'], ['falcon', 'eagle', 'hawk']],
  ['animal', 'subject', 'animal', 'الحيوان', ['حيوان', 'اسد', 'نمر', 'قطه', 'كلب', 'طائر', 'ذئب'], ['animal', 'lion', 'tiger', 'cat', 'dog', 'bird', 'wolf']],
  ['plane', 'subject', 'aircraft', 'الطائرة', ['طائره', 'طيران'], ['plane', 'airplane', 'aircraft', 'jet']],
  ['boat', 'subject', 'yacht', 'اليخت', ['يخت', 'قارب', 'سفينه'], ['yacht', 'boat', 'ship', 'sailboat']],
  ['robot', 'subject', 'robot', 'الروبوت', ['روبوت', 'انسان آلي'], ['robot', 'android', 'cyborg']],
  ['logo', 'subject', 'logo', 'الشعار', ['شعار', 'لوغو'], ['logo', 'brand mark']],
  // colours
  ['black', 'color', 'black', 'أسود', ['اسود', 'سوداء'], ['black']],
  ['white', 'color', 'white', 'أبيض', ['ابيض', 'بيضاء'], ['white']],
  ['red', 'color', 'red', 'أحمر', ['احمر', 'حمراء'], ['red']],
  ['blue', 'color', 'blue', 'أزرق', ['ازرق', 'زرقاء'], ['blue']],
  ['green', 'color', 'green', 'أخضر', ['اخضر', 'خضراء'], ['green']],
  ['gold', 'color', 'gold', 'ذهبي', ['ذهبيه', 'مذهب'], ['gold', 'golden']],
  ['silver', 'color', 'silver', 'فضي', ['فضي', 'فضيه'], ['silver', 'chrome']],
  ['yellow', 'color', 'yellow', 'أصفر', ['اصفر', 'صفراء'], ['yellow']],
  // places (proper nouns → reliable English transliteration)
  ['tokyo', 'place', 'Tokyo', 'طوكيو', ['طوكيو'], ['tokyo']],
  ['dubai', 'place', 'Dubai', 'دبي', ['دبي'], ['dubai']],
  ['riyadh', 'place', 'Riyadh', 'الرياض', ['الرياض'], ['riyadh']],
  ['jeddah', 'place', 'Jeddah', 'جدة', ['جده'], ['jeddah']],
  ['alula', 'place', 'AlUla', 'العلا', ['العلا'], ['alula', 'al ula']],
  ['abudhabi', 'place', 'Abu Dhabi', 'أبوظبي', ['ابوظبي', 'ابو ظبي'], ['abu dhabi']],
  ['doha', 'place', 'Doha', 'الدوحة', ['الدوحه'], ['doha']],
  ['cairo', 'place', 'Cairo', 'القاهرة', ['القاهره'], ['cairo']],
  ['istanbul', 'place', 'Istanbul', 'إسطنبول', ['اسطنبول'], ['istanbul']],
  ['paris', 'place', 'Paris', 'باريس', ['باريس'], ['paris']],
  ['london', 'place', 'London', 'لندن', ['لندن'], ['london']],
  ['newyork', 'place', 'New York', 'نيويورك', ['نيويورك'], ['new york', 'nyc', 'manhattan']],
  ['moscow', 'place', 'Moscow', 'موسكو', ['موسكو'], ['moscow']],
  ['maldives', 'place', 'the Maldives', 'المالديف', ['المالديف'], ['maldives']],
  ['redsea', 'place', 'the Red Sea', 'البحر الأحمر', ['البحر الاحمر'], ['red sea']],
  // lighting cues
  ['neon', 'light', 'neon lighting', 'إضاءة نيون', ['نيون'], ['neon', 'cyberpunk']],
  ['dramatic', 'light', 'dramatic lighting', 'إضاءة درامية', ['درامي', 'دراميه', 'ظلال'], ['dramatic', 'moody', 'chiaroscuro', 'low key', 'shadows']],
  ['volumetric', 'light', 'volumetric light', 'إضاءة حجمية', ['اشعه', 'حزم ضوء', 'خيوط الضوء', 'حجميه'], ['volumetric', 'god rays', 'light rays', 'light beams', 'sunbeams']],
  ['natural', 'light', 'natural light', 'إضاءة طبيعية', ['اضاءه طبيعيه', 'ضوء طبيعي'], ['natural light', 'natural lighting', 'available light']],
  ['candle', 'light', 'warm candle and practical light', 'إضاءة دافئة', ['شموع', 'شمعه', 'فوانيس', 'نار'], ['candle', 'candlelight', 'lantern', 'firelight', 'fireplace']],
  ['reflections', 'light', 'reflections', 'انعكاسات', ['انعكاس', 'انعكاسات', 'لامع'], ['reflection', 'reflections', 'glossy', 'mirror']],
  // camera cues
  ['c_drone', 'camera', 'drone', 'لقطة جوية', ['درون', 'جوي', 'جويه', 'من الاعلى', 'طائره مسيره'], ['drone', 'aerial', 'bird\'s eye', 'from above', 'overhead']],
  ['c_tracking', 'camera', 'tracking', 'لقطة تتبع', ['تتبع', 'متابعه', 'تلاحق'], ['tracking', 'follow shot', 'following']],
  ['c_slowmo', 'camera', 'slow motion', 'حركة بطيئة', ['حركه بطيئه', 'تصوير بطيء', 'سلو موشن', 'بالعرض البطيء'], ['slow motion', 'slow-motion', 'slowmo', 'slo-mo']],
  ['c_closeup', 'camera', 'close-up', 'لقطة قريبة', ['لقطه قريبه', 'قريبه', 'تفاصيل', 'ماكرو'], ['close-up', 'closeup', 'close up', 'macro', 'detail shot']],
  ['c_handheld', 'camera', 'handheld', 'كاميرا محمولة', ['محموله', 'كاميرا يد'], ['handheld', 'hand-held', 'shaky cam']],
  ['c_crane', 'camera', 'crane', 'لقطة رافعة', ['رافعه', 'كرين'], ['crane', 'jib']],
  ['c_dolly', 'camera', 'dolly', 'دوللي', ['دوللي', 'دولي', 'اقتراب بطيء'], ['dolly', 'push in', 'push-in', 'pull back']],
  ['c_orbit', 'camera', 'orbit', 'دوران حول العنصر', ['دوران', 'تدور الكاميرا', '360'], ['orbit', 'orbiting', '360', 'rotating around']],
  ['c_pan', 'camera', 'pan', 'بان', ['بان ', 'مسح افقي'], ['pan', 'panning']],
  ['c_wide', 'camera', 'wide', 'لقطة واسعة', ['واسعه', 'بانوراما', 'بانورامي'], ['wide shot', 'wide angle', 'panoramic', 'panorama']],
  // mood
  ['luxury', 'mood', 'luxurious, refined', 'فاخر', ['فاخر', 'فخم', 'فخامه', 'راقي', 'انيق', 'ترف'], ['luxury', 'luxurious', 'premium', 'elegant', 'high-end', 'upscale', 'refined']],
  ['epic', 'mood', 'epic, grand scale', 'ملحمي', ['ملحمي', 'مهيب', 'عظيم', 'اسطوري'], ['epic', 'grand', 'majestic', 'monumental', 'legendary']],
  ['calm', 'mood', 'calm, serene', 'هادئ', ['هادئ', 'هدوء', 'سكينه', 'استرخاء', 'مريح'], ['calm', 'serene', 'peaceful', 'tranquil', 'relaxing', 'quiet']],
  ['energetic', 'mood', 'high energy, fast paced', 'حماسي', ['حماسي', 'سريع', 'سرعه', 'نشاط', 'اثاره', 'مثير'], ['energetic', 'fast', 'fast-paced', 'dynamic', 'action', 'thrilling', 'speed']],
  ['mysterious', 'mood', 'mysterious, tense', 'غامض', ['غامض', 'غموض', 'تشويق', 'توتر'], ['mysterious', 'mystery', 'suspense', 'tense', 'thriller']],
  ['romantic', 'mood', 'romantic, intimate', 'رومانسي', ['رومانسي', 'حب', 'حميم'], ['romantic', 'love', 'intimate']],
  ['warm', 'mood', 'warm, inviting', 'دافئ', ['دافئ', 'دفء', 'كرم', 'ضيافه', 'حنين'], ['warm', 'cozy', 'inviting', 'hospitality', 'nostalgic']],
  ['futuristic', 'mood', 'futuristic', 'مستقبلي', ['مستقبلي', 'مستقبل', 'تقني', 'خيال علمي'], ['futuristic', 'sci-fi', 'science fiction', 'high-tech', 'cyberpunk']],
  ['joyful', 'mood', 'joyful, uplifting', 'مبهج', ['فرح', 'مبهج', 'سعاده', 'احتفال', 'بهجه'], ['joyful', 'happy', 'uplifting', 'celebration', 'cheerful', 'fun']],
  // realism / motion
  ['real', 'realism', 'photorealistic', 'واقعي', ['واقعي', 'واقعيه', 'حقيقي'], ['realistic', 'photorealistic', 'hyperrealistic', 'photoreal', 'lifelike']],
  ['moving', 'motion', 'subject in motion', 'حركة', ['تسير', 'تنطلق', 'يركض', 'تجري', 'يمشي', 'تحلق', 'يطير', 'تتحرك', 'يقود', 'تمر', 'يعدو', 'تبحر'], ['driving', 'running', 'walking', 'flying', 'racing', 'moving', 'speeding', 'riding', 'sailing', 'galloping']],
];

export function normalize(text) {
  return String(text || '')
    .replace(/[ً-ْٰـ]/g, '')
    .replace(/[أإآٱ]/g, 'ا').replace(/ى/g, 'ي').replace(/ة/g, 'ه')
    .replace(/\s+/g, ' ').toLowerCase().trim();
}
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const AR_PREFIX = '(?<![\\p{L}])(?:و|ف)?(?:ب|ل|ك)?(?:ال|لل)?';

const arStem = (s, group) => {
  const n = normalize(s);
  // proper nouns must match as whole words (الرياض must not match «الرياضية»)
  if (group === 'place') return `(?<![\\p{L}])(?:و|ف)?(?:ب|ل|ك)?${esc(n)}(?![\\p{L}])`;
  const bare = n.replace(/^ال/, '');
  return AR_PREFIX + esc(bare.length >= 3 ? bare : n);
};
export const concepts = raw.map(([id, group, en, ar, arStems, enStems]) => ({
  id, group, en, ar,
  re: new RegExp(
    `${arStems.map((s) => arStem(s, group)).join('|')}|(?<![\\p{L}])(?:${enStems.map(esc).join('|')})s?(?![\\p{L}])`, 'u'),
}));

export function detect(text) {
  const n = normalize(text);
  return concepts.filter((c) => c.re.test(n));
}
export const hasArabic = (t) => /[؀-ۿ]/.test(String(t || ''));
