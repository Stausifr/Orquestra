import useSWR from 'swr';
const fetcher = (url: string) => fetch(url).then(r => r.json());
export default function Home() {
  const { data: agents } = useSWR('/agents', fetcher);
  const { data: approvals } = useSWR('/approvals/pending', fetcher);
  return (
    <div className="p-4">
      <h1 className="text-xl">Orquestra Dashboard</h1>
      <div>Agents: {agents ? agents.length : '...'}</div>
      <div>Pending Approvals: {approvals ? approvals.length : '...'}</div>
    </div>
  );
}
