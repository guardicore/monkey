const mockStore = {
    '123': {id: '123', description: 'event 123'},
    '456': {id: '456', description: 'event 456'},
    '789': {id: '789', description: 'event 789'},
}
export default function Event({ params }: { params: { slug: string} }) {
  return <div>Event id: {params.slug} <br/>
              Event description: {mockStore[params.slug].description}</div>
}
