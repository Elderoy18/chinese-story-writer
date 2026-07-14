// dns-test.js
const dns = require('dns');
console.log('c-ares servers:', dns.getServers());
dns.resolveSrv('_mongodb._tcp.cluster0.bapvkdv.mongodb.net', (err, addrs) => {
  console.log('error:', err);
  console.log('addresses:', addrs);
});