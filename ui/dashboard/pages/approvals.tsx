import useSWR from 'swr';
const fetcher = (url: string) => fetch(url).then(r => r.json());
export default function Approvals() {
  const { data, mutate } = useSWR('/approvals/pending', fetcher);
  const act = async (id: number, action: string) => {
    await fetch(`/approvals/${id}/${action}`, { method: 'POST' });
    mutate();
  };
  return (
    <div className="p-4">
      <h1>Approvals</h1>
      <ul>
        {data && data.map((a: any) => (
          <li key={a.id}>{a.reason}
            <button onClick={() => act(a.id,'approve')}>Approve</button>
            <button onClick={() => act(a.id,'reject')}>Reject</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
