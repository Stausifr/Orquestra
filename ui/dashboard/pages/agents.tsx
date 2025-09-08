import useSWR from 'swr';
const fetcher = (url: string) => fetch(url).then(r => r.json());
export default function Agents() {
  const { data } = useSWR('/agents', fetcher);
  return (
    <div className="p-4">
      <h1>Agents</h1>
      <ul>
        {data && data.map((a: any) => (<li key={a.id}>{a.provider}:{a.name}</li>))}
      </ul>
    </div>
  );
}
