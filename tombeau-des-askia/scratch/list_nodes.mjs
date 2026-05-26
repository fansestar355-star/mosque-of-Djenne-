import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import draco3d from 'draco3dgltf';

const io = new NodeIO()
    .registerExtensions(ALL_EXTENSIONS)
    .registerDependencies({
        'draco3d.decoder': await draco3d.createDecoderModule(),
        'draco3d.encoder': await draco3d.createEncoderModule(),
    });

const doc = await io.read('assets/3d/Tombeaux_des_Askia.glb');
const root = doc.getRoot();

console.log('--- NODES ---');
for (const node of root.listNodes()) {
    const mesh = node.getMesh();
    console.log(`node: "${node.getName()}"${mesh ? ` -> mesh: "${mesh.getName()}"` : ''}`);
}
