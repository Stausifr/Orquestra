import { useEffect, useState } from 'react';
export default function Traces() {
  const [ticks, setTicks] = useState<number[]>([]);
  useEffect(() => {
    const evt = new EventSource('/metrics/live');
    evt.onmessage = e => {
      const data = JSON.parse(e.data);
      setTicks(t => [...t, data.tick]);
    };
    return () => evt.close();
  }, []);
  return <div className="p-4">Traces: {ticks.join(',')}</div>;
}
