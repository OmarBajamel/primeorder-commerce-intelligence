import Link from "next/link";
export default function NotFound() { return <div className="state-card"><strong>Page not found</strong><p>The requested dashboard view does not exist.</p><Link className="button secondary" href="/">Return to overview</Link></div>; }
