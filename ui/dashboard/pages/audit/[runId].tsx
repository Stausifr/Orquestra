import { useRouter } from 'next/router';
import useSWR from 'swr';
const fetcher = (url: string) => fetch(url).then(r => r.json());
export default function Audit() {
  const router = useRouter();
  const { runId } = router.query;
  const { data } = useSWR(runId ? `/audit/${runId}.json` : null, fetcher);
  return <pre className="p-4">{data ? JSON.stringify(data, null, 2) : '...'}</pre>;
}
