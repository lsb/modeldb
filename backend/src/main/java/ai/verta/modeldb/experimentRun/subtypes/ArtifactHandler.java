package ai.verta.modeldb.experimentRun.subtypes;

import ai.verta.modeldb.artifactStore.ArtifactStoreDAO;
import ai.verta.modeldb.common.futures.FutureJdbi;
import ai.verta.modeldb.datasetVersion.DatasetVersionDAO;

import java.util.concurrent.Executor;

public class ArtifactHandler extends ArtifactHandlerBase {
  public ArtifactHandler(
      Executor executor,
      FutureJdbi jdbi,
      String entityName,
      CodeVersionHandler codeVersionHandler,
      DatasetHandler datasetHandler,
      ArtifactStoreDAO artifactStoreDAO,
      DatasetVersionDAO datasetVersionDAO) {
    super(
        executor,
        jdbi,
        "artifacts",
        entityName,
        codeVersionHandler,
        datasetHandler,
        artifactStoreDAO,
        datasetVersionDAO);
  }
}
