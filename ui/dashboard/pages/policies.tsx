import useSWR from 'swr';
const fetcher = (url: string) => fetch(url).then(r => r.json());
export default function Policies() {
  const { data } = useSWR('/policies', fetcher);
  return (
    <div className="p-4">
      <h1>Policies</h1>
      <ul>
        {data && data.map((p: string) => (<li key={p}>{p}</li>))}
      </ul>
    </div>
  );
}
