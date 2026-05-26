const fs = require('fs');
const path = require('path');

const root = 'c:\\Users\\Kabakoo Apprenant.e\\Desktop\\MES PROJETS\\tombeau-des-askia';
const glbPath = path.join(root, 'assets', '3d', 'Tombeaux_des_Askia.glb');

if (!fs.existsSync(glbPath)) {
    console.error('File not found:', glbPath);
    process.exit(1);
}

const buffer = fs.readFileSync(glbPath);
const content = buffer.toString('utf8');

const names = ['Tombeaux', 'La_base', 'Espace_des_femmes', 'Espace_des_hommes', 'Branche', 'Haute_parleur'];
console.log('--- MESH CHECK ---');
names.forEach(name => {
    // Check for common variations like spaces or underscores
    const found = content.includes(name);
    if (found) {
        console.log(`[OK] Found "${name}"`);
    } else {
        console.log(`[MISSING] "${name}"`);
    }
});
