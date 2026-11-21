const P = {
  play: 'M7 5l12 7-12 7z', pause: 'M7 5h4v14H7zM13 5h4v14h-4z', plus: 'M12 5v14M5 12h14', x: 'M6 6l12 12M18 6L6 18',
  check: 'M5 12.5l4.5 4.5L19 7.5', up: 'M6 14l6-6 6 6', down: 'M6 10l6 6 6-6', trash: 'M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13',
  copy: 'M9 9h10v11H9zM5 15V4h10', refresh: 'M4 12a8 8 0 0114-5.3L20 9M20 4v5h-5M20 12a8 8 0 01-14 5.3L4 15M4 20v-5h5',
  spark: 'M12 3l1.8 5.4L19 10l-5.2 1.6L12 17l-1.8-5.4L5 10l5.2-1.6zM19 16l.7 2.1L22 19l-2.3.9L19 22l-.7-2.1L16 19l2.3-.9z',
  film: 'M4 5h16v14H4zM8 5v14M16 5v14M4 9.5h4M4 14.5h4M16 9.5h4M16 14.5h4', grid: 'M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z',
  user: 'M12 12a4 4 0 100-8 4 4 0 000 8zM4.5 20a7.5 7.5 0 0115 0', shield: 'M12 3l7 3v5.5c0 4.3-2.9 7.6-7 9.5-4.1-1.9-7-5.2-7-9.5V6z',
  download: 'M12 4v11M7 11l5 5 5-5M5 20h14', share: 'M8 12l8-5M8 12l8 5M6 14.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5zM18 9a2.5 2.5 0 100-5 2.5 2.5 0 000 5zM18 20a2.5 2.5 0 100-5 2.5 2.5 0 000 5z',
  edit: 'M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4', upload: 'M12 16V5M7 9l5-5 5 5M5 20h14', camera: 'M3 8h4l2-3h6l2 3h4v11H3zM12 17a3.5 3.5 0 100-7 3.5 3.5 0 000 7z',
  sun: 'M12 16a4 4 0 100-8 4 4 0 000 8zM12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8',
  palette: 'M12 3a9 9 0 000 18c1.4 0 2-1 2-2 0-1.5 1-2 2.3-2H18a3 3 0 003-3c0-6-4-11-9-11zM7.5 12.5h.01M9.5 8h.01M14.5 7.5h.01',
  link: 'M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1', alert: 'M12 4l9 16H3zM12 10v4.5M12 17.5v.01',
  music: 'M9 18V6l10-2v12M9 18a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zM19 16a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z', volume: 'M4 10v4h4l5 4V6l-5 4zM16.5 9a4 4 0 010 6M19 6.5a8 8 0 010 11',
  mute: 'M4 10v4h4l5 4V6l-5 4zM17 9.5l4 5M21 9.5l-4 5', full: 'M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5', logout: 'M14 4h5v16h-5M10 8l-4 4 4 4M6 12h9',
  globe: 'M12 21a9 9 0 100-18 9 9 0 000 18zM3 12h18M12 3c2.5 2.5 3.5 5.5 3.5 9S14.5 18.5 12 21c-2.5-2.5-3.5-5.5-3.5-9S9.500 5.5 12 3z',
  menu: 'M4 7h16M4 12h16M4 17h16', layers: 'M12 3l9 5-9 5-9-5zM3 13l9 5 9-5M3 17.500l9 5 9-5', clock: 'M12 21a9 9 0 100-18 9 9 0 000 18zM12 7v5l3 2',
  image: 'M4 5h16v14H4zM4 16l5-5 4 4 3-3 4 4M9 9.500h.01', drag: 'M9 6h.01M15 6h.01M9 12h.01M15 12h.01M9 18h.01M15 18h.01', cog: 'M12 15a3 3 0 100-6 3 3 0 000 6zM19 12l2-1.500-2-3.500-2.300.900a7 7 0 00-1.700-1L14.500 4h-5l-.500 2.900a7 7 0 00-1.700 1L5 7 3 10.500 5 12l-2 1.500L5 17l2.300-.900a7 7 0 001.700 1L9.500 20h5l.500-2.900a7 7 0 001.700-1L19 17l2-3.500z',
  arrow: 'M5 12h14M13 6l6 6-6 6', info: 'M12 21a9 9 0 100-18 9 9 0 000 18zM12 11v6M12 7.500v.01',
};
/** Line icons. `flip` mirrors direction-dependent icons (arrows) in RTL. */
export function Icon({ name, size = 18, flip = false, ...rest }) {
  return (
    <svg className={flip ? 'ico flip' : 'ico'} width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...rest}>
      <path d={P[name] || P.info} />
    </svg>
  );
}
