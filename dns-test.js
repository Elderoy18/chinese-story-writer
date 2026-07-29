const dns = require('dns');
const { Resolver } = require('dns');

const host = '_mongodb._tcp.cluster0.nxgekpd.mongodb.net';
console.log('default c-ares servers:', dns.getServers());

dns.resolveSrv(host, (err, addrs) => {
  console.log('\n[default resolver]',
    err ? 'FAILED: ' + err.code : 'OK — found ' + addrs.length + ' nodes');
});

const r = new Resolver();
r.setServers(['1.1.1.1', '8.8.8.8']);
r.resolveSrv(host, (err, addrs) => {
  console.log('[forced 1.1.1.1]',
    err ? 'FAILED: ' + err.code + '  <- external DNS blocked on this network'
        : 'OK — found ' + addrs.length + ' nodes  <- the setServers fix works here');
});



// // dns-test.js
// const dns = require('dns');
// console.log('c-ares servers:', dns.getServers());
// dns.resolveSrv('_mongodb._tcp.cluster0.bapvkdv.mongodb.net', (err, addrs) => {
//   console.log('error:', err);
//   console.log('addresses:', addrs);
// });