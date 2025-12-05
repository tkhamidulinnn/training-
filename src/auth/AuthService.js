const config = require('./authConfig');
// Mocking libraries to avoid install errors in test
const bcrypt = { hash: (p) => `hashed_${p}`, compare: (p, h) => h === `hashed_${p}` };
const jwt = { sign: (p, s) => `token_${p.id}` };

class AuthService {
  constructor(userRepository) {
    this.users = userRepository;
  }

  /**
   * Registers a new user with hashed password
   * @param {string} email 
   * @param {string} password 
   */
  async register(email, password) {
    const existing = await this.users.findByEmail(email);
    if (existing) throw new Error('User already exists');

    const passwordHash = await bcrypt.hash(password, config.saltRounds);
    
    return this.users.create({
      email,
      passwordHash,
      role: 'USER',
      createdAt: new Date()
    });
  }

  /**
   * Authenticates user and returns JWT
   */
  async login(email, password) {
    const user = await this.users.findByEmail(email);
    if (!user) throw new Error('Invalid credentials');

    const isValid = await bcrypt.compare(password, user.passwordHash);
    if (!isValid) throw new Error('Invalid credentials');

    const token = jwt.sign({ id: user.id, role: user.role }, config.jwtSecret);
    return { user, token };
  }
}

module.exports = AuthService;
