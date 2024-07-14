const DATA = {
    id: 1,
    label: 'AAAAA',
    style: { color: '#fff', background: '#108ffe' },
    children: [
      {
        id: 2,
        pid: 1,
        label: 'SDDDDDD',
        style: { color: '#fff', background: '#108ffe' },
        children: [
          { id: 6, pid: 2, label: 'FSDFDD', disabled: true },
          { id: 8, pid: 2, label: 'FFDDSF', noDragging: true },
          { id: 10, pid: 2, label: 'SDFSDFSDF' },
        ],
      },
      {
        id: 3,
        pid: 1,
        label: 'EEFSD',
        style: { color: '#fff', background: '#108ffe' },
        children: [
          { id: 11, pid: 3, label: 'SDFDDDD' },
          { id: 12, pid: 3, label: 'GGGGG' },
        ],
      },
      {
        id: 4,
        pid: 1,
        label: 'GGGGG',
        style: { color: '#fff', background: '#108ffe' },
      },
    ],
  };
  
  export default DATA;
  