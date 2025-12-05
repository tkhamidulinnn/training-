module.exports = {
  jwtSecret: process.env.JWT_SECRET || 'super_secret_key_dev',
  jwtExpiration: '1h',
  saltRounds: 10,
  requireEmailVerification: true
};
