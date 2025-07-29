export interface Config {
  /**
   * Plugin name. Must be unique.
   */
  name: 'my-zod';
  /**
   * Name of the generated file.
   *
   * @default 'my-plugin'
   */
  output?: string;
  /**
   * User-configurable option for your plugin.
   *
   * @default false
   */
  myOption?: boolean;
}
